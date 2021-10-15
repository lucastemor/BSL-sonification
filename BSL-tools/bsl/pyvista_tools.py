import pyvista as pv 
import numpy as np

def get_ids_in_section(model,section,inverse=False,check_surface=True):
	'''
	given full model and some geometry section, get model IDs that interset with section
	somewhat similar to a custom clip
	if inverse, we get ids that are outside of the section
	'''

	if inverse == False:
		intersection_ids = np.where(model.select_enclosed_points(section,check_surface=check_surface).point_arrays['SelectedPoints'] == 1)[0]
	else:
		intersection_ids = np.where(model.select_enclosed_points(section,check_surface=check_surface).point_arrays['SelectedPoints'] == 0)[0]

	return intersection_ids


def convert_vtk(fpath,out_type):
	from pathlib import Path

	if out_type[0] == '.':
		out_type = out_type[1:]

	fpath = Path(fpath)
	outdir = Path(fpath.parent).joinpath(f'{out_type}_{fpath.stem}')

	if outdir.exists() == False:
		outdir.mkdir(parents=True)

	for i,file in enumerate(fpath.glob('*.vt*')): #vtu,vtp, vtk
		print (f'Converting file {i+1}', end='\r')
		step = pv.read(file)
		step.save(outdir.joinpath(f'{file.stem}.{out_type}') )



