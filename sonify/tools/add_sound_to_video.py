""" Render sonification and add to video frames or existing video
Will create new folder /BSL-sonification/output/{case}_{video_name}_{iter_name}-{n_existing} for output

Parameters
----------
case : str
	name of Aneurisk case
video_path : str
	path to visualization video. If .mp4 extension, sound will be rendered, scaled, and added to existing video.
	If no extension, it is assumed to be a path to .png frames. Desired video must be specified and video frames will be rendered
video_length : str, conditional
	Needed if video_path is for a directory of .png frames rather than a file, see video_path for more
iter_name : str, optional
	If you want to append a unique identifier to the output directory - eg., if 'foo' is passed folder name will be /*_foo/

Returns
-------

Notes
-----

ignoring for now -- figuring out sound generation first 
changed where this file lives  -- make sure to change all paths etc
probably iwll not need to be run from commmand line in future anyways 

"""

import sys, glob, os, shutil
from pathlib import Path
from sonify.synth_classes.python_synthdefs import *
from matplotlib import image as mplimage
import matplotlib.pyplot as plt


def render_video_from_frames(path_to_frames,desired_length,render_name):
	frames = list(video_path.glob('*.png'))
	fps = len(frames)/float(desired_length)
	resolution = mplimage.imread(frames[0]).shape
	res = f'{resolution[0]}x{resolution[1]}'
	pic_name = str(video_path.joinpath(frames[0].stem[:-4])) #assumes all frames are padded with 4 zeros eg.,  my_pic.0001
	video_path = str(path_to_frames.joinpath(f'{render_name}.mp4'))

	os.system(f'ffmpeg -r {fps} -f image2 -s {res} -i {pic_name}%04d.png -vcodec libx264 -crf 25 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -pix_fmt yuv420p {video_path}')

	return video_path

def add_tracks_to_video(video_path,outdir,itername,*audio_paths):

	temp_outfile = outdir.joinpath('temp_audio.wav')
	shutil.copy(str(audio_paths[0]), str(temp_outfile))

	n_audio=len(audio_paths)

	if n_audio == 1:
		outfile = audio_paths[0]
	else:
		outfile = outdir.joinpath('mix_out.wav')

	for i in range(n_audio)[1:]:
		os.system(f'ffmpeg -y -i {str(temp_outfile)} -i {str(audio_paths[i])} -filter_complex amix=inputs=2:duration=longest {str(outfile)}')
		shutil.copy(str(outfile), str(temp_outfile))

	os.remove(str(temp_outfile))
	os.system(f'ffmpeg -y -i {str(video_path)} -i {str(outfile)} -filter:a "volume=2" -map 0 -map 1 -c:a aac {str(outdir.joinpath(f"{itername}_final.mp4"))}')



if __name__ == '__main__':
	"""
	convenient way to sonify with desired synthdef and sync the sound to the video frames
	"""
	
	#for quick debugging purposes, args are hardcoded if not specified.
	try:
		case 		 = sys.argv[1]
		video_path 	 = sys.argv[2]
		video_length = sys.argv[3]
		iter_name 	 = sys.argv[4] #note to set to '' if none passed
	except:
		#case = 'c0053'
		#video_path = Path('/home/lucas/Documents/viz/renders/Matrix_iterations/aneurisk/c0053/waveform_matrix._60fps_1stride.mp4' )
		
		case = 'c0004'
		video_path = Path('/home/lucas/Documents/viz/renders/Matrix_iterations/aneurisk/c0004/pathq.mp4')


		#case = 'c0032'
		#video_path = Path('/home/lucas/Documents/viz/renders/Matrix_iterations/aneurisk/c0032/waveform_matrix2-2._60fps_1stride.mp4')

		#case = 'c0060'
		#video_path = Path('/home/lucas/Documents/viz/renders/Matrix_iterations/aneurisk/c0060/c0060waveform_matrix2-2._60fps_1stride.mp4')

		iter_name = 'flat_q_chroma_frequencymod'
		video_length = 20


	########### GENERAL I/O SETUP #################################################

	base_path = Path('/home/lucas/Documents/BSL-sonification')

	render_name = f'{case}_{video_path.stem}_{iter_name}'
	outdir = base_path.joinpath('output',case,render_name)

	if outdir.exists() == False:
		outdir.mkdir(parents=True)
	else:
		n_existing = len(list(outdir.parent.glob(f'*{render_name}*')))
		outdir = base_path.joinpath('output',case,f'{render_name}-{n_existing}')
		outdir.mkdir(parents=True)

	########### SETTING UP VIDEO PARAMS  ##############################################################

	#if a folder of frames is specified, we render the video at the given deisred lenghth, and update video_path to match the newly rendered video
	#if a vidoe file is specified, we want to update video_length to be the same length as the given video
	if video_path.suffix == '':
		video_path = render_video_from_frames(video_path,video_length,render_name)
	else: 
		video_length = float(os.popen(f'ffprobe -i {video_path} -show_entries format=duration -v quiet -of csv="p=0"').read())


	############## SONIFICATION I/O & WAV RENDERING #######################################

	q_array 	= np.load(base_path.joinpath('data','aneurisk','flat_q_data',case,'master_sonification_q.npy'))
	r_array 	= np.load(base_path.joinpath('data','aneurisk','flat_q_data',case,'master_sonification_r.npy'))

	Pxx_scaled  = np.load(base_path.joinpath('data','aneurisk','spectrograms',case,'sac_averaged','sac_spectro_filtered_scaled.npy'))
	bins 		= np.load(base_path.joinpath('data','aneurisk','spectrograms',case,'sac_averaged','bins.npy'))
	freqs 		= np.load(base_path.joinpath('data','aneurisk','spectrograms',case,'sac_averaged','freqs.npy'))	


	filtered_chromagram		= np.load(base_path.joinpath('data','aneurisk','chromagrams',case,'sac','filt_chroma.npy'))

	'''
	flat_q_synth = flat_q_with_spectro_env(q_array,r_array,Pxx_scaled,bins,freqs)
	flat_q_synth.looptime = video_length
	flat_q_sound_file = outdir.joinpath('flat_q.wav')
	flat_q_synth.listen(path=flat_q_sound_file)
	flat_q_sound_file = outdir.joinpath('flat_q_rescale.wav')

	chroma_synth = timbral_chromagram('four_osc_chromagram',filtered_chromagram)
	chroma_synth.looptime = video_length
	chroma_synth.send_to_sc()
	chroma_sound_file = outdir.joinpath('chromagram_features.wav')
	chroma_synth.listen(path=chroma_sound_file) 
	
	add_tracks_to_video(video_path,outdir,iter_name,flat_q_sound_file,chroma_sound_file)
	'''

	
	flat_q_chroma = flat_q_with_spectro_env_chromagram(q_array,r_array,Pxx_scaled,bins,freqs,filtered_chromagram)
	flat_q_chroma.looptime = video_length
	flat_q_chroma_sound_file = outdir.joinpath('flat_q_chroma.wav')
	flat_q_chroma.listen(path=flat_q_chroma_sound_file)
	flat_q_chroma_sound_file = outdir.joinpath('flat_q_chroma_rescale.wav')

	add_tracks_to_video(video_path,outdir,iter_name,flat_q_chroma_sound_file)
	

	'''
	fig,ax  = plt.subplots(3,1,figsize= (9,16))

	ax[0].pcolormesh(bins,freqs,Pxx_scaled,shading='gouraud')
	ax[1].pcolormesh(bins,np.arange(0,12),filtered_chromagram,shading='auto',vmin=0,vmax=1)
	ax[2].pcolormesh(bins,np.arange(0,12),flat_q_chroma.chroma_features,shading='auto',vmin=0,vmax=1)

	fig.suptitle(case)
	ax[0].set_title('Spectrogram, filtered, scaled')
	ax[1].set_title('Chromagram')
	ax[2].set_title('Chromagram feature mask')

	plt.savefig(outdir.joinpath(f'{case}_plots.png'))
	plt.cla()
	plt.close()
	'''


	sonification iteration -- flat q + spectrogam envelope (mapped to turbine buffeting sound) + chromagram (mapped to string-like sound).
	Trying a new way of blending the two sounds by modulating the frequency of the pitched sounds with the noisey turbine signal.
	Aesthetics are still sometimes irritating (c0053 sounds like a horror movie soundtrack haha)
	Will discuss more tomorrow. 
