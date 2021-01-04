"""
Computation of chromagram and feature detection, plus plotting utilities
"""

import librosa
import numpy as np 
import matplotlib.pyplot as plt
from skimage import filters as skf
from skimage import exposure as ske
import bsl



def load_mesh_and_matrix(mesh_path,df_path):
	
	mesh = bsl.io.read_mesh_data(mesh_path)
	df = np.array(bsl.io.read_pd_dataframe(df_path))

	return mesh, df

def get_sampled_points(mesh,df, sample_density = 0.5):
	sampler = bsl.sampling.SpectrogramSampler(df,mesh)
	sampler.sample_mode = 'random_sample'
	sampler.sample_density = sample_density
	sampler.set_probe(sampler.surface)
	sampler.generate_sample_ids()
	sampler.sample_data()

	return sampler

def get_unscaled_spectro(sampler,filtered=False,lowcut=25):

	if filtered:
		data = bsl.filters.filter_time_data(sampler.df_sampled,sampler.fs,lowcut=lowcut,btype='highpass')
	else:
		data = sampler.df_sampled

	Pxx_ave, _, freqs,bins = bsl.spectral.get_average_spectrogram(data,fs=sampler.fs)

	return Pxx_ave, freqs, bins

def get_chroma_features(Pxx_filtered,Pxx_unfiltered,n_chroma_bins, fs):
	
	filt_unfilt_features = []
	
	for spectrogram in [Pxx_filtered,Pxx_unfiltered]:
		chromagram = librosa.feature.chroma_stft(S=spectrogram,n_chroma=n_chroma_bins, tuning=0,sr=fs)

		sobel_x = skf.sobel(chromagram,axis=0)
		sobel_y = skf.sobel(chromagram,axis=1)
		sobel_mag = np.hypot(sobel_x,sobel_y)

		diff=  chromagram - sobel_mag
		floored_diff = np.where(diff<=0,0,diff)	

		diff_gradient_x = np.where(skf.sobel(floored_diff,axis=0) <0,0,skf.sobel(floored_diff,axis=0)) #laZY, MAKE A NEW VARIALE 

		clahe = ske.equalize_adapthist(diff_gradient_x,kernel_size=10,clip_limit=0.01)
		clahe_thresh = np.where(clahe>0.25,clahe,0)

		clahe_max_only = np.zeros_like(clahe_thresh)
		for i,column in enumerate(clahe_thresh.T):
			pitch_class_with_max_value = np.argmax(column)
			clahe_max_only[pitch_class_with_max_value,i] = clahe_thresh[pitch_class_with_max_value,i] 

		filt_unfilt_features.append(clahe_max_only)

	filtered_features 	= filt_unfilt_features[0]
	unfiltered_features = filt_unfilt_features[1]

	non_zero_filtered  	= filtered_features >0
	non_zero_unfiltered = unfiltered_features > 0

	intersection = non_zero_unfiltered == non_zero_filtered
	
	#filtered used here intersection here, but either could be used as the intersection is equal for filt and unfilt
	filtered_intersection = np.where(intersection,filtered_features,0)

	return filtered_intersection


def get_chromagram_features(mesh_path,df_path,n_chroma_bins,sample_density = 0.5):
	"""
	Helper function to load data, compute chromagram, detect features, and prepare features to be sent to sc for sonification

	"""

	mesh,df = load_mesh_and_matrix(mesh_path, df_path)
	spectro_sampler = get_sampled_points(mesh,df,sample_density)

	Pxx_ave_unfiltered, freqs, bins = get_unscaled_spectro(spectro_sampler, filtered=False)
	Pxx_ave_filtered, _,_ = get_unscaled_spectro(spectro_sampler,filtered=True)
	
	chromagram_features = get_chroma_features(Pxx_ave_filtered,Pxx_ave_unfiltered,n_chroma_bins,spectro_sampler.fs)

	return chromagram_features, bins





