"""
Utilities for preprocessing data before it is sent to supercolider
"""

from bsl import spectrogram_features
import scipy.ndimage as ndimage
import numpy as np

def n_octa_arpeggio(n,groupID,shift): #n octave 'arpeggio'
    
    fundamental=220
    
    while groupID>n:
        groupID-=n
    
    fifths = np.arange(8,100,12)
    noteID = (groupID-1)*4

    if noteID in fifths:
        noteID -=1
    
    freq = chroma(noteID,shift,fundamental)
    
    return(freq)

def chroma(noteID,shift,fundamental):
    if shift == 0:
        return(fundamental*(2**(noteID/12.00)))
    else:
        return(fundamental*(2**((noteID+shift)/12.00)))


def getPitches(blob):

	structure1 = np.array([[1,1,1],
                      	   [1,1,1],
                           [1,1,1]])

	structure2 = np.array([[0,1,0],
                           [1,1,1],
                           [0,1,0]])


	dial = ndimage.binary_dilation(blob, structure=structure2).astype(blob.dtype)


	labeled_array,num_features = ndimage.label(dial,structure=structure1)
	#masked_label = blob*labeled_array #thin line representations
	masked_label=labeled_array.copy() #blob representations

	dict = {}

	for idx,col in enumerate(masked_label.T):
		nonzero_index = np.nonzero(col)
		label = col[nonzero_index]

		for j in range(0,len(label)):
		    if label[j] not in dict.keys():                                   		#if the first instance of the group
		        dict[label[j]] =  (nonzero_index[0][j])                       		#map its group id to its starting row
		        col[nonzero_index[0][j]] = n_octa_arpeggio(9,label[j],shift=0)             #assign it an initial frequency
		    else:                                                            		#else get how far away it is from its inital frequency
		        difference = nonzero_index[0][j] - dict[label[j]]             		#difference is where it is - where it started
		        col[nonzero_index[0][j]] = n_octa_arpeggio(9,label[j],shift=0.5*difference)#difference) 	#frequency is original freq plus difference # of half steps     


	return(masked_label,labeled_array)


def get_Pxx_blob_features(Pxx,freqs):

	envelope = spectrogram_features.get_envelope(Pxx.copy(),freqs)

	bands,relativePeakHeight, extrapolated_envelope = spectrogram_features.get_bands_and_extrapolation(Pxx.copy(),freqs)
	active = np.where(bands<0,1,0)

	pitches, plotLabels = getPitches(active)

	return active, envelope, pitches, plotLabels, relativePeakHeight