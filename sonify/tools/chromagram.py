"""
Computation of chromagram and feature detection, plus plotting utilities
"""

import librosa, bsl, glob, os
import numpy as np 
import matplotlib.pyplot as plt
from skimage import filters as skf
from skimage import exposure as ske


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


def columnwise_threshold(chroma,max_min_diff,thresh,inverse=False):
	"""
	mask chromagram based on threshold condition from its column
	"""
	if inverse:
		masking_col = np.where(max_min_diff>thresh,0,1)
	else:
		masking_col = np.where(max_min_diff>thresh,1,0)
	return chroma*masking_col

def column_max_mask(chroma):
	"""
	keep only max column value, 0s elsewhere
	"""
	chroma_max_only = np.zeros_like(chroma)
	for i,column in enumerate(chroma.T):
		row_with_max_value = np.argmax(column)
		chroma_max_only[row_with_max_value,i] = chroma[row_with_max_value,i]

	return chroma_max_only


def get_chromagram_features(chromagram):

	sobel_x = skf.sobel(chromagram,axis=0)
	sobel_y = skf.sobel(chromagram,axis=1)
	sobel_mag = np.hypot(sobel_x,sobel_y)

	diff = chromagram - sobel_mag
	floor_diff = np.where(diff<=0,0,diff)

	sum_masked = columnwise_threshold(floor_diff,np.sum(floor_diff,axis=0),thresh=7,inverse=True)
	max_features = column_max_mask(sum_masked)

	return np.where(max_features!=0,chromagram,0)



def get_chroma_features_from_Pxx(Pxx_filtered,n_chroma_bins, fs):
	
	chromagram  = librosa.feature.chroma_stft(S=Pxx_filtered,  n_chroma=n_chroma_bins, tuning=0,sr=fs)
	chromagram_features = get_chromagram_features(chromagram)

	return filtered_intersection

'''
#old, no lopnger in use -> simpler feature pipeline above
def get_chromagram_features(chromagram_filtered,chromagram_unfiltered):
	
	filt_unfilt_features = []
	
	for chromagram in [chromagram_filtered,chromagram_unfiltered]:
		sobel_x = skf.sobel(chromagram,axis=0)
		sobel_y = skf.sobel(chromagram,axis=1)
		sobel_mag = np.hypot(sobel_x,sobel_y)

		diff=  chromagram - sobel_mag
		floored_diff = np.where(diff<=0,0,diff)	

		#this is messy, fix later
		#don't want to compute x grad anymore, just skipping over this now
		diff_gradient_x = floored_diff#np.where(skf.sobel(floored_diff,axis=0) <0,0,skf.sobel(floored_diff,axis=0)) #laZY, MAKE A NEW VARIALE 

		clahe = ske.equalize_adapthist(diff_gradient_x,kernel_size=10,clip_limit=0.01)
		clahe_thresh = np.where(clahe>0.5,clahe,0)

		clahe_max_only = np.zeros_like(clahe_thresh)
		for i,column in enumerate(clahe_thresh.T):
			pitch_class_with_max_value = np.argmax(column)
			clahe_max_only[pitch_class_with_max_value,i] = clahe_thresh[pitch_class_with_max_value,i] 

		original_chromagram_masked = np.where(clahe_max_only>0, chromagram,0)
		filt_unfilt_features.append(original_chromagram_masked)

	filtered_features_masked_chromagram 	 = filt_unfilt_features[0]
	unfiltered_features_masked_chromagram    = filt_unfilt_features[1]

	non_zero_filtered  	= filtered_features_masked_chromagram   > 0
	non_zero_unfiltered = unfiltered_features_masked_chromagram > 0

	intersection = non_zero_unfiltered == non_zero_filtered
	
	filtered_intersection = np.where(intersection,filtered_features_masked_chromagram,0)

	return filtered_intersection
'''

'''
#old, not used anymore -> loading data and computing spectro/chroma should be done elsewhere
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

'''

if __name__ =='__main__':
	"""
	Bulk compute filtered and unfiltered chromagrams
	"""

	data_path = '/home/lucas/Documents/BSL-sonification/data/aneurisk/spectrograms/'
	chromagram_path = '/home/lucas/Documents/BSL-sonification/data/aneurisk/chromagrams/'

	sampling = 'sac' # sac or full_model

	cases = glob.glob(data_path+'c*')

	for case in cases:
		name = os.path.split(case)[1]
		outdir = chromagram_path+name+'/'+sampling
		os.makedirs(outdir,exist_ok=True)

		if sampling == 'full_model':
			mesh_path = f'{data_path}/{name}/{name}.vtu'
			df_path   = f'{data_path}/{name}/{name}.h5'

			mesh,df = load_mesh_and_matrix(mesh_path, df_path)
			spectro_sampler = get_sampled_points(mesh,df,sample_density=100)

			Pxx_ave_unfiltered, freqs, bins = get_unscaled_spectro(spectro_sampler, filtered=False)
			Pxx_ave_filtered, _,_ = get_unscaled_spectro(spectro_sampler,filtered=True)

			np.save(outdir+'/freqs.npy',		  freqs)
			np.save(outdir+'/bins.npy',			  bins)
			np.save(outdir+'/unfilt_spectro.npy', Pxx_ave_unfiltered)
			np.save(outdir+'/filt_spectro.npy',   Pxx_ave_filtered)

		elif sampling == 'sac':
			Pxx_ave_unfiltered = np.load(f'{data_path}/{name}/sac_averaged/sac_spectro_unfiltered.npy')   
			Pxx_ave_filtered   = np.load(f'{data_path}/{name}/sac_averaged/sac_spectro_filtered.npy')

		unfiltered_chromagram = librosa.feature.chroma_stft(S=Pxx_ave_unfiltered,n_chroma=12, tuning=0,sr=2500/0.951)
		filtered_chromagram   = librosa.feature.chroma_stft(S=Pxx_ave_filtered  ,n_chroma=12, tuning=0,sr=2500/0.951)
		
		np.save(outdir+'/unfilt_chroma.npy',  unfiltered_chromagram)
		np.save(outdir+'/filt_chroma.npy',    filtered_chromagram)


		Pxx_scaled_unfiltered = bsl.spectral.spectrogram_scaling(Pxx_ave_unfiltered.copy(),lower_thresh = -20)
		Pxx_scaled_filtered   = bsl.spectral.spectrogram_scaling(Pxx_ave_filtered.copy(),  lower_thresh = -20)

		fig, ax = plt.subplots(3,2,figsize=(15,15))
		fig.suptitle(name)

		bins = np.arange(0,filtered_chromagram.shape[1])
		freqs =np.arange(0,Pxx_ave_unfiltered.shape[0]) 

		ax[0][0].pcolormesh(bins,freqs,Pxx_ave_unfiltered,shading = 'gouraud')
		ax[0][0].set_title('Unfiltered spectorgram')

		ax[0][1].pcolormesh(bins,freqs,Pxx_ave_filtered, shading = 'gouraud')
		ax[0][1].set_title('Filtered spectorgram')

		ax[1][0].pcolormesh(bins,freqs,Pxx_scaled_unfiltered,shading = 'gouraud')
		ax[1][0].set_title('Unfiltered spectorgram, scaled')

		ax[1][1].pcolormesh(bins,freqs,Pxx_scaled_filtered, shading = 'gouraud')
		ax[1][1].set_title('Filtered spectorgram, scaled')

		ax[2][0].pcolormesh(bins,np.arange(0,12),unfiltered_chromagram, shading = 'auto')
		ax[2][0].set_title('Unfiltered chromagram')

		ax[2][1].pcolormesh(bins,np.arange(0,12),filtered_chromagram, shading = 'auto')
		ax[2][1].set_title('Filtered chromagram')

		plt.savefig(outdir+'/plots.png')
		plt.cla()
		plt.close()