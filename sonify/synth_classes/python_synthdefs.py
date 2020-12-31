"""
Classes for different synthdefs - this is where new classes will be added to interface with precompiled synthdefs made in supercollider 
Each class inherits synth.precompute or synth.realtime depending on how data is sent to sc and how the synthdef is written (see synth.py documentation for more info)

"""

from . import synth
from sonify.tools.spectro_harmonic_preprocessing import get_Pxx_blob_features
import numpy as np

class Pxx_blob(synth.precompute):
	"""
	Feature based spectrogram sonification. Synth similar to what was submitted to cancelled ICAD 2020.
	Harmonic bands are extracted using peak detection and sonified with sin osc
	Spectrogram envelop extracted and sonified using noise sweep

	Attributes
	-----------------
	synthdef : str
		Synthdef saced in sc.sc.synthdefpath - precompiled in supercollider. Default here is Pxx_blob which is similar to the ICAD 2020 submission synth
	
	freqs : 1-D numpy array  
		Range of frequencies form spectrogram - used for feature detection functions

	bins : 1-D numpy array
		Time bins - needs to be the same as what is in the synthdef (36 bins is convention for spectrograms). Each time bin will have a unique sound, and they are played in sequence to make the sonification

	pxx : 2-D numpy array 
		Spectrogram to be sonified (dimensions freqs.shape x bins.shape)

	active : 2-D numpy array 
		Denotes which oscilators to keep on - the same non-zero entries as pitches. This holds whether the pitch is on or off (dimensions freqs.shape x bins.shape)
 
	noise : 1-D numpy array
		Array of cutoff frequencies for the LPF with noise input in supercolider. Computed based on spectrogram envelope.

	pitches : 2-D numpy array
		Denotes the pitches of the active oscillators. Harmonic sounds are forced by assigning notes of major triad for stacked harmonics. See preprocessing.getPitches for more info

	labels : 2-D numpy array
		for visualizing pitch blob groups

	relativePeakHeight: 2-D numpy array
		Height of detected spectrogram bands with respect to overall power falloff. Used to control panning in synthdef
	"""

	def __init__(self, pxx, freqs, bins):
		super().__init__()
		self.synthdef = 'Pxx_blob'
		self.freqs = freqs
		self.bins  = bins

		self.pxx = pxx
		self.active = None
		self.noise = None
		self.pitches = None
		self.labels = None
		self.relativePeakHeight = None

		self.generate_synthlist()

	def send_to_sc(self):
		"""
		Detect features and send the matricies to supercollider
		Important to note that you cannot iterate over numpy arrays to send to sc -- must be converted to a list first
		"""
		self.active,self.noise,self.pitches, self.labels, self.relativePeakHeight  =  get_Pxx_blob_features(self.pxx.copy(),self.freqs)

		freqs = self.freqs.tolist()
		cut_row = self.noise.tolist()
		n_bins = len(self.bins)

		for idx,syn in enumerate(self.synthlist):
			if idx < self.freqs.shape[0]:
				pxx_row = self.relativePeakHeight[idx].tolist()
				act_row = self.active[idx].tolist() 				#which harmonics are active
				pitch_row = self.pitches[idx].tolist() 				#pitch of active harmonics
				syn.timestretch = self.looptime

				param_names 	= ['cut_','pxx_','act_','ph_']
				param_values 	= [cut_row,pxx_row,act_row,pitch_row]

			#exception (i.e., if there are more synths in the synthlist than there are spectrogram dimensions) if envelope synth (eg., click) is to be appeneded to the end of synthlist 
			else:
				param_name = 'cut_'
				param_value = cut_row

			for param_name,param_value in zip(param_names,param_values): #this loop replaces the hardcoding of each time bin. This is where we set the class attributes on the sc server
				names = [f'{param_name}{str(step).zfill(3)}' for step in range(n_bins)]
				for name,value in zip(names,param_value):
					syn.__setattr__(name,value)


class flat_q_with_spectro_env(synth.realtime):

	def __init__(self,q_array,r_array,pxx,bins,freqs):
		super().__init__()
		self.synthdef = 'flat_q_with_spectro_env'

		self.q_array = q_array
		self.r_array = r_array
		
		self.pxx = pxx
		self.bins = bins

		self.n_positions = q_array.shape[0]
		
		positions = np.linspace(0,1,int(self.n_positions/2) + 1) #temp variable
		self.positions = np.append(positions,-1*np.flip(positions[1:-1]))

		self.n_timesteps = q_array.shape[1]

		_, self.envelope,_,_,_ = get_Pxx_blob_features(self.pxx.copy(),freqs) #this is probably an uncessary bottleneck - just compute envelope directly in future

		#rescale and interpolate cutoff frequency envelope over all video frames
		self.envelope /=2
		self.interp_envelope = np.interp(np.linspace(0,self.bins.max(),self.n_timesteps),self.bins,self.envelope)

		#just to maintain naming convention - needed for synthlist generation.. sor for the confusion 
		self.freqs = np.zeros(self.n_positions)
		
		self.generate_synthlist()

		#this doesn't need to be updated in realtime, only computed once, so we'll do it here
		for each in range (self.n_positions):
			self.synthlist[each].theta = float(self.positions[each])

	def send_to_sc(self,timestep):
		"""
		Unlike precompute - this is called multiple times in the loop as recording progresess. 
		Done for each step in range self.n_timesteps -> see synth.realtime for more
		Assumes all computed on python client side
		"""
		for position,syn in enumerate(self.synthlist):
			syn.q = float(self.q_array[position][timestep]) #+ interp_envelope[timestep])
			syn.r = float(self.r_array[position][timestep])
			syn.e = float(self.interp_envelope[timestep])