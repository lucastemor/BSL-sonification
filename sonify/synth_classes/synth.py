"""

Main class for sonification -- all sonification mappings (e.g., flat_q, resynth, etc) will inherit this class
These classes aren't really used directly, just parent classes for the classes in python_synthdefs.py

"""

import sc,pyaudio,wave,time,os
import numpy as np
from pathlib import Path

class synth:
	""" Class for general supercollider initialization. Inherited by precomputed and realtime synths
	
	Attributes
	-----------------

	audio_device : str
		changes depending on os, run debug script to brute force all devices with pyaudio	
	synthdef : str 
		Name of synthdef saved in sc.sc.synthdefpath - precompiled in supercollider
	synthlist : list
		for most applications we want to stack multiple synths, this list will contain them. Index 0 is the bottom of the stack
	freqs : 1-D numpy array
		Generally used to assign attributes to vertically stacked synths in synthlist - Naming convention inherited from  Dan's spectral synthesis where freqs represented the freqency bins from the FFT.
	bins : 1-D numpy array
		Generally used as the time indicies - Naming convention inherited from Dan's sonifications, similar to freqs but for time bins	 		
	looptime : float
		Playback lenght for the precomputed sound
	
	"""

	def __init__(self):
		print ('Initializing SuperCollider ... ')
		
		#sc.boot_and_connect() #?not working right now, for the time being, do this manually -> not recording properly
		
		sc_path = '/Applications/SuperCollider.app/Contents/Resources/scsynth'
		sc.sc.start(sc_path, startscsynth=0)
		sc.sc.synthdefpath = '/Users/BSL/Documents/BSL-sonification/supercollider/synthdefs' 

		self.audio_device = 'Loopback Audio'#'pulse' (linux?) #'Soundflower (2ch)' --> for mac
		self.synthdef = None
		self.synthlist = []	
		self.freqs = None
		self.bins = None

		self.looptime= 5

	def add_synth(self,synthdef):
		""" Append new synthdef to the synthlist

		Parameters
		----------------
		
		synthdef : str
			name of synthdef to append

		"""
		syn = sc.sc.Synth(synthdef)
		self.synthlist.append(syn)
		syn.outBus = 0

	def generate_synthlist(self):
		""" Generate synthlist containing len(freqs) synths - can think of them as vertically stacked

		"""
		for each in range(len(self.freqs)):
			self.add_synth(self.synthdef)

	def append_synths(self, *new_synthdef_names):
		""" Convenience function for adding multiple new synthdefs

		Parameters
		----------------
		*new_synthdef_names : str
			name of synthdefs to append (*args)

		"""
		for synthdef in new_synthdef_names:
			self.add_synth(synthdef)


	def free(self, kill_servers=False):
		"""
		Free all synths on the supercollider server - this is the same as pressing ctrl+. in supercollider

		Parameters
		-------------

		kill_servers : bool
			If true, will shutdown the server after nodes are freed 
		"""
		for each in self.synthlist:
			each.free()

		if kill_servers:
			sc.kill_servers()

	def get_input_device_number(self):
		"""
		For recording

		Returns
		-----------
		input_device_number : int
			device number corresponding to given self.audio_device name
		"""
		p = pyaudio.PyAudio()
		info = p.get_host_api_info_by_index(0)
		numdevices = info.get('deviceCount')

		input_device_number = 9999

		for i in range(0, numdevices):
				device = p.get_device_info_by_host_api_device_index(0, i)
				if device.get('maxInputChannels') > 0 and device.get('name') == self.audio_device:
					input_device_number = int(i)

		if input_device_number == 9999:
			print (f'Input Device {self.audio_device} Not Found!')
		else:
			return input_device_number


class precompute(synth):
	""" Precompute sound and playback - useful for spectrogram/chromagram sonification.
		Can quickly repeat sounds by toggling gate open/close
		A fast way to sonify matricies, and precise with time scaling
		but won't work for large number of timesteps (e.g., 1200) as supercollider will have memory issues,
		and the synthdef is a pain to write.

		Important to stick to naming conventions here (e.g., timestretch, freqshift, fr_000) when writing synthdef in supercollider
	"""

	def open_gate(self):
		"""
		Begin playback after the sound has been precomputed
		"""
		for s in self.synthlist:
			s.gate = 1.0
			s.timestretch = self.looptime
			s.freqshift = 0.0

	def close_gate(self):
		"""
		Stops playback
		"""
		for s in self.synthlist:
			s.gate = 0.0

	def listen(self,path=None):
		"""Open the gate to playback the sound. If a path is specified, a .wav recording will also be saved.

		Parameters
		---------------

		path : str, optional 
			If specified, a recording of the sound will be saved to this path. Make sure self.audop_device is working - and see lib/troubleshoot_audio.py if not
		"""
		if self.synthlist == []:
			self.synthlist = self.generate_synthlist()
	
		if path!= None:
			FORMAT = pyaudio.paInt16
			CHANNELS = 2
			CHUNK = 1024
			RATE = 44100
			RECORD_SECONDS = self.looptime
			WAVE_OUTPUT_FILENAME = str(path)

			audio = pyaudio.PyAudio()

			stream = audio.open(format=FORMAT, channels=CHANNELS,
							rate=RATE, input=True,
							frames_per_buffer=CHUNK, input_device_index=self.get_input_device_number())

			print("recording...")

			frames=[]
			self.open_gate()

			for i in range(0, int(RATE / CHUNK * (self.looptime) )+8):
				data = stream.read(CHUNK)
				frames.append(data)

			stream.stop_stream()
			stream.close()
			audio.terminate()
			waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
			waveFile.setnchannels(CHANNELS)
			waveFile.setsampwidth(audio.get_sample_size(FORMAT))
			waveFile.setframerate(RATE)
			waveFile.writeframes(b''.join(frames))
			waveFile.close()

			print ('done!')
			self.free()
		else:
			self.open_gate()




class realtime(synth):
	"""Docs

	its more pseudo realtime -- because assumes precomputed on client (python) side
	maybe there is a way to mnake it flexible to also just get realtime datastream from python
	though this isn't reall useful? 
	"""

	def rescale_audio(self,path,desired_length):
		path = Path(path)
		fname= str(path)
		out = str(path.parent.joinpath(path.stem + '_rescale.wav'))

		actual_length = float(os.popen(f'ffprobe -i {path} -show_entries format=duration -v quiet -of csv="p=0"').read())
		atempo = actual_length / desired_length
		os.system(f'ffmpeg -y -i {fname} -filter:a "atempo={atempo}" -vn {out}')


	def listen(self,path=None):
		"""
		Very similar to precompute.listen but the realtime playback and recording have to
		update simultaneously - this means that we can't just open a gate as with precompute.listen,
		rather we need to keep track of recording chunks and send new data to supercollider simultaneously 
		In future can probably offload some repeated code to main synth class

		Important: the self.send_to_sc function is defined at the lowest class lecel (i.e., in python_synthdefs.py)
		as each synthdef will send different data in diffrent ways
		"""

		if self.synthlist == []:
			self.synthlist = self.generate_synthlist()
	
		if path!= None:
			FORMAT = pyaudio.paInt16
			CHANNELS = 2
			CHUNK = 1024
			RATE = 44100
			RECORD_SECONDS = self.looptime
			WAVE_OUTPUT_FILENAME = str(path)

			audio = pyaudio.PyAudio()

			stream = audio.open(format=FORMAT, channels=CHANNELS,
							rate=RATE, input=True,
							frames_per_buffer=CHUNK, input_device_index=self.get_input_device_number())

			print("recording...")

			frames=[]
			
			for timestep in range(self.n_timesteps):
				self.send_to_sc(timestep=timestep) 	# this is a function unique to each synthdef
				data = stream.read(CHUNK)
				frames.append(data)

				time.sleep(0.01) #not 100% sure about this yet -- how to control timing 

			stream.stop_stream()
			stream.close()
			audio.terminate()

			self.free()

			waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
			waveFile.setnchannels(CHANNELS)
			waveFile.setsampwidth(audio.get_sample_size(FORMAT))
			waveFile.setframerate(RATE)
			waveFile.writeframes(b''.join(frames))
			waveFile.close()

			print ('done!')
			self.free()

			self.rescale_audio(WAVE_OUTPUT_FILENAME,self.looptime)

		else:
			for timestep in range(self.n_timesteps):
				self.send_to_sc(timestep=timestep)
				time.sleep(0.01)
			self.free() 