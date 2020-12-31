"""
Mostly for developement -- load a sample case and sonify using different techniques
Eventually this can become an example or useful for wrapping everything
"""

from sonify.synth_classes.python_synthdefs import Pxx_blob, flat_q_with_spectro_env
from pathlib import Path
import numpy as np

if __name__ == '__main__':

	#load some data -- e.g., sac spectrogram
	data_path = Path('/home/lucas/Documents/BSL-sonification/data/aneurisk/spectrograms/c0053')

	Pxx_scaled = np.load(data_path.joinpath('sac_spectro.npy'))
	freqs = np.load(data_path.joinpath('freqs.npy'))
	bins = np.load(data_path.joinpath('bins.npy'))

	q_array = np.load('/home/lucas/Documents/sonification/flat_q_data/c0053/master_sonification_q.npy')
	r_array = np.load('/home/lucas/Documents/sonification/flat_q_data/c0053/master_sonification_r.npy')


	#include this here or in class __init__  ??
	r_array /= r_array.max()
	q_array *= 3.5	

	flat_q_test = flat_q_with_spectro_env(q_array,r_array,Pxx_scaled,bins,freqs)
	flat_q_test.looptime = 10
	#we don't need to call send for realtime - the listen method will do this for us
	flat_q_test.listen(path='flat_q_test.wav')

	'''
	synth = Pxx_blob(Pxx_scaled,freqs,bins)
	synth.looptime = 10
	synth.send_to_sc()
	synth.listen(path = 'test.wav')
	'''