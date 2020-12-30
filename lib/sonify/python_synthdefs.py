"""
Classes for different synthdefs - this is where new sounds will  added
Each class inherits synth.precompute or synth.realtime depending on how data is sent to sc
basically, depends on number of timesteps, if there are many (e.g., 1250) sc will not have enough memory to precompute, so realtime is the only option)
"""

from . import synth

class Pxx_blob(synth.precompute):

	def __init__(self):
		super().__init__()
		self.synthdef = 'Pxx_blob'
		self.generate_synthlist()
		self.pxx = None
		self.active = None
		self.noise = None
		self.pitches = None
		self.labels = None
		self.relativePeakHeight = None


	def send_spectro(self):
		if self.synthdef != 'resynth':
			self.active,self.noise,self.pitches, self.labels, self.relativePeakHeight  =  get_sonification_parameters(self.pxx.copy(),self.freqs)

			freqs = self.freqs.tolist()
			cut_row = self.noise.tolist()
			n_harmonics_row = np.zeros(self.pxx.shape[1])
			n_bins = len(self.bins)

			for idx,syn in enumerate(self.synthlist):
				if idx < self.freqs.shape[0]: 
					syn.fr_000 = freqs[idx]
					pxx_row = self.relativePeakHeight[idx].tolist() #reletive height
					act_row = self.active[idx].tolist() #which harmonics are active
					pitch_row = self.pitches[idx].tolist() #pitch of active harmonics
					syn.timestretch = self.looptime

					param_names = ['cut_','pxx_','act_','ph_']
					param_values = [cut_row,pxx_row,act_row,pitch_row]

				else: #exception for when envelope synth (eg., click) is appeneded to the end of synthlist
					param_name = 'cut_'
					param_value = cut_row

				for param_name,param_value in zip(param_names,param_values): #this loop replaces the hardcoding of each time bin 
					names = [f'{param_name}{str(step).zfill(3)}' for step in range(n_bins)]
					for name,value in zip(names,param_value):
						syn.__setattr__(name,value)
		else:
			#add for resynthsis i.e., Dan style synth that skips feature detection
			pass 
