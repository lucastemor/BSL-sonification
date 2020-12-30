""" Render sonification and add to video frames or existing video
Will create new folder /BSL-sonification/output/{video_name} for output
If folder exists, _n will be appended with n being the number of cases+1


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

"""

import sys, glob
from pathlib import Path


def test():
	"""
	This is a test function and it works -- updating the docs 
	"""
	return


if __name__ == '__main__':
	
	#for quick debugging purposes, args are hardcoded if not specified.
	try:
		case 		 = sys.argv[1]
		video_path 	 = sys.argv[2]
		video_length = sys.argv[3]
		iter_name 	 = sys.argv[4] #note to set to '' if none passed
	except:
		case = 'c0053'
		video_path = Path('/home/lucas/Documents/viz/renders/Matrix_iterations/aneurisk/c0053added_waveform/waveform_matrix._60fps_1stride.mp4' )
		iter_name = '_testing'

	render_name = f'{case}_{video_path.stem}_{iter_name}'
	outdir = Path('output').joinpath(render_name)
	if outdir.exists() == False:
		outdir.mkdir()
	else:
		n_existing = len(glob.glob(f'output/*{render_name}*'))
		outdir = Path('output').joinpath(f'{render_name}-{n_existing}')
		outdir.mkdir(parents=True)
