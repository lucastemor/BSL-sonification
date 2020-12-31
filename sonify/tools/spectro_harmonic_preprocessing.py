"""
Utilities for preprocessing harmonics extraxcted from spectrograms data before it is sent to supercolider. 
Feature detection, and assignment of pitches to detected haronic bands

Notes
-----------------
This is old and sloppy code that works but could be improved.

"""

from bsl import spectrogram_features
import scipy.ndimage as ndimage
import numpy as np

def n_octa_arpeggio(n,groupID,shift, fundamental=220):
	"""Determine where in the major chord the passed frequency sits. We also impose a perceptual boundary
	at which the frequency stack of triad notes resets so we don't have something like the 24th detected band being a triad frequency that
	is exteremly high pitched. 

	
	Parameters
	--------------------
	n : int
		number of octaves we will limit the frequency range to
		This is a perceptual consideration - we don't want to synthesize frequencies outside of the range of human hearing

	groupID : int
		passed from the feature detection. These correspond to the vertically stacked bands.
		Each representing root, third, or fifth in arpeggio
		e.g., for fundamental 220 some sample groupID inputs are as follows 1,2,3,4,5,6 will give A3, C#4, E4, A4, C#5, E5, respectively

	shift : float 
		for synthesizing glissando like effects when the frequencies falloff.
		See documentation for preprocessing.chroma for more info.

	fundamental : float, optional
		Default = 220. The starting note upon which to build the n octave arpeggio 

	Returns
	--------------------
	freq: float
		frequency at which to sonify the band based on major triad frequencies, bounded within n octaves.

	"""


	'''
	this is how we reassign notes that fall above the octave limit.
	so if we have a group id that would be assigned to A10 (arbitrary, any high pitch), this will knock it down to
	something lower, e.g., A5 (these values aren't tested, just illustrating the concept)
	'''
	while groupID>n:
	    groupID-=n

	"""
	Converting the triad position to respective chromatic scale position
	E.g., we have 1,2,3 which correspond to root, third, fifth, respectively
	Need to transform these into chromatic scale ids within the correct octave. 
	In general, root, third, fifth correspond to chromatic scale notes 0, 4, 7
	Adustment is made for the fifth as spacing is different
	"""
	noteID = (groupID-1)*4

	fifths = np.arange(8,100,12)
	if noteID in fifths:
	    noteID -=1

	freq = chroma(noteID,shift,fundamental)

	return(freq)

def chroma(noteID,shift,fundamental):
	"""Compute the frequency of the nth note in the chromatic scale with stating note frequency `fundamental`
	Option to shift the pitch if glissando effect desired.

	Parameters
	----------------
	noteID : int 
		The nth note of the chromatic scale. E.g., if fundamental is A4 (440 Hz) and 11 is passed for noteID
		the frequency for G#5 will be returned. If 23 is passed, the frequency for G#6 will be returned, etc.

	shift : float
		Allows for defining the frequency of notes in between notes of 12 tone equal temperament chromatic scale.
		For example, if we have fundamental = 440 , noteID = 1, and shift = 0.5, we will get the frequency of the
		note that is between A4 and A#4 (in this case, allows to get the quartertone)

	Fundamental : float
		Starting note of the chromatic scale we are computing. E.g., fundamental = 440 will start chromatic scale at A4 


	Returns
	------------------
	frequency : float
		The frequency of the requested note on the chromatic scale

	"""
	if shift == 0:
		return(fundamental*(2**(noteID/12.00)))
	else:
		return(fundamental*(2**((noteID+shift)/12.00)))


def getPitches(blob):
	"""Once we have detected bands in the spectrogram, detect each unique band and assign it a frequency corresponding to a major triad.

	Parameters
	------------------------
	blob : 2-D numpy array
		This should be the binarized/skeletonized array of detected harmonics from the spectrogram.


	Returns
	-----------------------
	masked_label : 2-D numpy array
		Array of frequencies to send to supercollider oscillators. Same shape as spectrogram.
		Each detected band is assigned a pitch such that stacked bands will form a major chord. 
		If bands decay in frequency this will be reflected in the changes in pitch (i.e., glissando)

	labeled_array : 2-D numpy array
		Labels frolm ndimage.label. Same shape as spectrogram. Useful for visualizing what groups were detected by the algorithm.
		Not used for sonification, rather as a visual sanity check / generating figures

	"""

	'''
	We want  to be able to detect continuous bands, but sometimes there are small gaps in the data, meaning more bands are detected than visually perceived. 
	These gaps would generally not really be considered by the visual system, as it would just look for continuity of bands, however the computer doesnt think this way...
	So the workaround for this is to just dialate every band so that these small discontinuities are filled. 
	There are two possible dialation structures below -> I (Lucas) ended up using structure2 to dialate but feel free to experiment.
	Take a look at the ndimage.binary_deialation docs for more info. 
	'''
	structure1 = np.array([[1,1,1],
                      	   [1,1,1],
                           [1,1,1]])

	structure2 = np.array([[0,1,0],
                           [1,1,1],
                           [0,1,0]])


	dial = ndimage.binary_dilation(blob, structure=structure2).astype(blob.dtype)

	'''
	With ndimage.label we are basically searching for connected pixel regions. Because everything is binarized this is pretty straightforward.
	We can also specify the search structure -> I found thast structure1 works best for this.
	'''
	labeled_array,num_features = ndimage.label(dial,structure=structure1)
	#masked_label = blob*labeled_array #thin line representations 
	masked_label=labeled_array.copy() #blob representations

	unique_label_dict = {}

	for idx,col in enumerate(masked_label.T):
		nonzero_index = np.nonzero(col)
		label = col[nonzero_index]

		#for each nonzero label
		for j in range(0,len(label)):
			#if the first instance of the group label
		    if label[j] not in unique_label_dict.keys():

		    	#map its group id to its starting row                                   		
		        unique_label_dict[label[j]] =  (nonzero_index[0][j])

		        #assign it an initial frequency based on major triad notes                       		
		        col[nonzero_index[0][j]] = n_octa_arpeggio(9,label[j],shift=0)

		    #else get how far away it is from its inital frequency - e.g, how much the band has decayed after systole             
		    else:
		    	#difference is where it is - where it started                                                            		
		        difference = nonzero_index[0][j] - unique_label_dict[label[j]]    
		        #frequency is original freq plus difference # of half steps          		
		        col[nonzero_index[0][j]] = n_octa_arpeggio(9,label[j],shift=0.5*difference)	    


	return(masked_label,labeled_array)


def get_Pxx_blob_features(Pxx,freqs):
	"""Helper function to compute spectrogram features for sonification, and assign sonification parameters to them (e.g., pitch)

	Parameters
	------------------
	Pxx : 2-D numpy array
		Generally a spectrogram - featrues will be detected on this
	freqs : 1-D numpy ARRAY
		Frequency bins from the fft 

	Returns
	----------------
	active : 2-D numpy array
		Same shape as spectrogram - will either contain a 1 if harmonics were detected at that point or a 0 otherwise
		Used to trun on/of the corresponding oscillator in supercollider

	envelope : 1-D numpy array
		Frequencies corresponding to outer edge of spectrogram

	pitches : 2-D numpy array
		Same shape as spectrogram. Same non-zero entries as active (i.e., non-zero where harmonics are detected)
		Used to set the frequency of the oscillator that is turned on by active

	plotLavels: 2-D numpy array
		Haven't used this in some time - dimensions should be the same as the spectrogram.
		See preprocessing.getPitches documentation for labeled_array
		I am pretty sure this assigns a unique ID number to each detected spectrogram band, so when plotted you can see how the algorithm has detected each group 
	
	relativePeakHeight : 2-D numpy array
		Same shape as spectrogram. For the peaks detected in each time bin power trace, get their relative height with respect to the interpolated power falloff

	"""
	envelope = spectrogram_features.get_envelope(Pxx.copy(),freqs)

	bands,relativePeakHeight, extrapolated_envelope = spectrogram_features.get_bands_and_extrapolation(Pxx.copy(),freqs)
	active = np.where(bands<0,1,0)

	pitches, plotLabels = getPitches(active)

	return active, envelope, pitches, plotLabels, relativePeakHeight