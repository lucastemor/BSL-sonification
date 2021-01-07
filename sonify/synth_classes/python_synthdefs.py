"""
Classes for different synthdefs - this is where new classes will be added to interface with precompiled synthdefs made in supercollider 
Each class inherits synth.precompute or synth.realtime depending on how data is sent to sc and how the synthdef is written (see synth.py documentation for more info)

"""

from . import synth
import numpy as np

from sonify.tools.spectro_harmonic_preprocessing import get_Pxx_blob_features
from sonify.tools.chromagram import get_chromagram_features

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

		self.features_computed = False

		self.generate_synthlist()


	def compute_features(self):
		self.active,self.noise,self.pitches, self.labels, self.relativePeakHeight  =  get_Pxx_blob_features(self.pxx.copy(),self.freqs)
		self.features_computed = True

	def send_to_sc(self):
		"""
		Detect features and send the matricies to supercollider
		Important to note that you cannot iterate over numpy arrays to send to sc -- must be converted to a list first
		"""
		if self.features_computed == False:
			self.compute_features()

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
	"""
	Flat mapped q-criterion sonificationwith spectrogram envelope modulation.
	synth.realtime is needed as we are working with every simulation timestep instead of a small number of time bins
	"""

	def __init__(self,q_array,r_array,pxx,bins,freqs):
		super().__init__()
		self.synthdef = 'flat_q_with_spectro_env'

		r_array /= r_array.max()
		q_array *= 3.5	

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
		During playback, this is what is called by synth.realtime (parent class) 
		Done for each step in range self.n_timesteps -> see synth.realtime for more
		Assumes all computed on python client side
		"""
		for position,syn in enumerate(self.synthlist):
			syn.q = float(self.q_array[position][timestep]) #+ interp_envelope[timestep])
			syn.r = float(self.r_array[position][timestep])
			syn.e = float(self.interp_envelope[timestep])


class simple_chromagram(synth.precompute):
	"""
	Chromagram feature based sonification. Map detected features to a simple sine osc
	Works only with global transposed_matrix, loaded directly
	in future implement a class to sample 
	"""

	def __init__(self, chromagram_filtered):
		"""
		Important that Pxx is not the scaled Pxx 
		"""
		super().__init__()
		self.synthdef = 'simple_chromagram'
		self.chromagram_filtered   = chromagram_filtered
		self.features_computed = False

		self.starting_note = 261.63 #middle c, in hz
		self.n_chroma_bins = 12 #chromatic scale, 12 pitches
		self.freqs =  [(self.starting_note*2**(i/self.n_chroma_bins)) for i in range (0,self.n_chroma_bins)] #limited to 1 octave

		self.generate_synthlist()

	def compute_features(self):
		self.chroma_features = get_chromagram_features(self.chromagram_filtered)
		self.features_computed = True

	def send_to_sc(self):
		if self.features_computed == False:
			self.compute_features()

		for i, syn in enumerate(self.synthlist):
			syn.fr_000 = self.freqs[i]

			pitch_row = self.chroma_features[i].tolist()
			param_names = ['ph_']
			param_values = [pitch_row]

			for param_name,param_value in zip(param_names,param_values): #this loop replaces the hardcoding of each time bin 
				names = [f'{param_name}{str(step).zfill(3)}' for step in range(self.chromagram_filtered.shape[1])]
				for name,value in zip(names,param_value):
					syn.__setattr__(name,value)


class timbral_chromagram(synth.precompute):
	"""
	Chromagram feature based sonification. Map detected features to a simple sine osc
	Works only with global transposed_matrix, loaded directly
	in future implement a class to sample 
	"""

	def __init__(self, timbre_synthdef, chromagram_filtered):
		"""
		Important that Pxx is not the scaled Pxx 
		"""
		super().__init__()
		self.synthdef = timbre_synthdef
		self.chromagram_filtered   = chromagram_filtered
		self.features_computed = False

		self.starting_note = 261.63 #middle c, in hz
		self.n_chroma_bins = 12 #chromatic scale, 12 pitches
		self.freqs =  [(self.starting_note*2**(i/self.n_chroma_bins)) for i in range (0,self.n_chroma_bins)] #limited to 1 octave

		self.generate_synthlist()

	def compute_features(self):
		self.chroma_features = get_chromagram_features(self.chromagram_filtered)
		self.features_computed = True

	def send_to_sc(self):
		if self.features_computed == False:
			self.compute_features()

		for i, syn in enumerate(self.synthlist):
			syn.fr_000 = self.freqs[i]

			pitch_row = self.chroma_features[i].tolist()
			param_names = ['ph_']
			param_values = [pitch_row]

			for param_name,param_value in zip(param_names,param_values): #this loop replaces the hardcoding of each time bin 
				names = [f'{param_name}{str(step).zfill(3)}' for step in range(self.chromagram_filtered.shape[1])]
				for name,value in zip(names,param_value):
					syn.__setattr__(name,value)


class flat_q_with_spectro_env_chromagram(synth.realtime):
	"""
	Flat mapped q-criterion sonificationwith spectrogram envelope modulation with blended / amplitude modulated chromagram pitches
	synth.realtime is needed as we are working with every simulation timestep instead of a small number of time bins
	"""

	def __init__(self,q_array,r_array,pxx,bins,freqs,chromagram_filtered):
		super().__init__()
		self.synthdef = 'flat_q_with_spectro_env_chromagram'

		r_array /= r_array.max()
		q_array *= 3.5	

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


		#precompute the chromagram features here, plus initialize pitches  
		self.chroma_features = get_chromagram_features(chromagram_filtered)
		self.starting_note = 440#261.63 #middle c, in hz
		self.n_chroma_bins = 12 #chromatic scale, 12 pitches
		self.pitches =  [(self.starting_note*2**(i/self.n_chroma_bins)) for i in range (0,self.n_chroma_bins)] #limited to 1 octave

		chroma_pitch_matrix = (np.array(self.pitches) * np.where(self.chroma_features>0,1,0).T)

		#project 36 time bin chromagram onto 1250 timestep q-data
		repeat_factor = np.ceil(self.n_timesteps/self.bins.shape[0])
		self.pitches_to_send = chroma_pitch_matrix.repeat(repeat_factor,axis=0)#NOTE axis 0 used because we have transpose from above

		#just to maintain naming convention - needed for synthlist generation for the q arrays.. sorry for the confusion 
		self.freqs = np.zeros(self.n_positions)
		
		self.generate_synthlist()

		#this doesn't need to be updated in realtime, only computed once, so we'll do it here
		for each in range (self.n_positions):
			self.synthlist[each].theta = float(self.positions[each])

	def send_to_sc(self,timestep):
		"""
		Unlike precompute - this is called multiple times in the loop as recording progresess.
		During playback, this is what is called by synth.realtime (parent class) 
		Done for each step in range self.n_timesteps -> see synth.realtime for more
		Assumes all computed on python client side
		"""
		for position,syn in enumerate(self.synthlist):
			syn.q = float(self.q_array[position][timestep]) #+ interp_envelope[timestep])
			syn.r = float(self.r_array[position][timestep])
			syn.e = float(self.interp_envelope[timestep])
			syn.pitch = float(self.pitches_to_send[timestep].max())