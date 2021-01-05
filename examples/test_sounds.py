"""
Mostly for developement -- load a sample case and sonify using different techniques
Eventually this can become an example or useful for wrapping everything
"""

from sonify.synth_classes.python_synthdefs import *
from pathlib import Path
import numpy as np
import bsl

import matplotlib.pyplot as plt

def get_unscaled_spectro(path,filtered=False,sample_density = 0.4):
	"""
	Load unscaled average spectrogram

	Parameters
	----------

	path : PosixPath 
		path to case folder. Expected formatting is as follows:
		path of PosixPath object is */{case}, i.e, path.stem = case
		Files in case directroy are aranged as follows:
		*/{case}/{case}.h5 for simulation matrix and */{case}/{case}.vtu for geo
	"""
	case = path.stem

	transposed_matrix = path.joinpath(case+'.h5')
	geometry_file = path.joinpath(case+'.vtu')

	df = np.array(bsl.io.read_pd_dataframe(transposed_matrix))
	mesh = bsl.io.read_mesh_data(geometry_file)

	sampler = bsl.sampling.SpectrogramSampler(df,mesh)
	sampler.sample_mode = 'random_sample'
	sampler.sample_density = sample_density
	sampler.set_probe(sampler.surface)
	sampler.generate_sample_ids()
	sampler.sample_data()
	
	Pxx_ave, _, freqs,bins = bsl.spectral.get_average_spectrogram(sampler.df_sampled,fs=sampler.fs)

	return Pxx_ave, freqs, bins


if __name__ == '__main__':

	#load some data -- e.g., sac spectrogram
	data_path = Path('/home/lucas/Documents/BSL-sonification/data/aneurisk/spectrograms/c0053')

	Pxx_scaled = np.load(data_path.joinpath('sac_spectro.npy'))
	freqs = np.load(data_path.joinpath('freqs.npy'))
	bins = np.load(data_path.joinpath('bins.npy'))

	q_array = np.load('/home/lucas/Documents/sonification/flat_q_data/c0053/master_sonification_q.npy')
	r_array = np.load('/home/lucas/Documents/sonification/flat_q_data/c0053/master_sonification_r.npy')

	chromagram_filtered   = np.load('/home/lucas/Documents/BSL-sonification/data/aneurisk/chromagrams/c0053/sac/filt_chroma.npy')
	chromagram_unfiltered = np.load('/home/lucas/Documents/BSL-sonification/data/aneurisk/chromagrams/c0053/sac/unfilt_chroma.npy')

	#Uncomment this block to test Pxx_blob
	'''
	synth = Pxx_blob(Pxx_scaled,freqs,bins)	
	synth.looptime = 10
	synth.send_to_sc()
	synth.listen(path = 'test.wav')
	'''

	#Uncomment this block to test flat q with spectro envelope

	flat_q_test = flat_q_with_spectro_env(q_array,r_array,Pxx_scaled,bins,freqs)
	flat_q_test.looptime = 10
	#we don't need to call send for realtime - the listen method will do this automatically
	flat_q_test.listen(path='flat_q_test.wav')

	#uncomment to test simple chromagram
	'''
	synth = simple_chromagram(chromagram_filtered,chromagram_unfiltered)
	synth.looptime = 5
	synth.send_to_sc()
	synth.listen() 
	'''

	'''
	fig, ax = plt.subplots(3,1,figsize=(5,10))


	ax[0].pcolormesh(synth.chromagram_unfiltered,shading='auto',vmin=0,vmax=1)
	ax[1].pcolormesh(synth.chromagram_filtered,shading='auto',vmin=0,vmax=1)
	ax[2].pcolormesh(synth.chroma_features,shading='auto',vmin=0,vmax=1)

	plt.show()
	'''