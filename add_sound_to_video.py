	""" Render sonification and add to video frames or existing video

	Parameters
	----------
	case : str
		name of Aneurisk case
	video_path : str
		path to visualization video. If .mp4 extension, sound will be rendered, scaled, and added to existing video.
		If no extension, it is assumed to be a path to .png frames. Desired video must be specified and video frames will be rendered
	video_length : str, conditional
		Needed if video_path is for a directory of .png frames rather than a file, see video_path for more

	Returns
	-------

	Notes
	-----

	"""

import sys
from pathlib import Path


def test():
	"""
	This is a test function and it works -- updating the docs 
	"""
	return


if __name__ == '__main__':
	
	#for quick debugging purposes, args are hardcoded if not specified.
	try:
		case = sys.argv[1]
		video_path = sys.argv[2]
	except:
		case = 'c0053'
		video_path = Path('/home/lucas/Documents/viz/renders/Matrix_iterations/aneurisk/c0053added_waveform/waveform_matrix._60fps_1stride.mp4' )

	
	render_name = video_path.stem
	outdir = Path('output').joinpath(render_name)
	if outdir.exists() == False:
		outdir.mkdir(parents=True)
