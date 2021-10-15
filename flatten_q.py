'''
Might throw up error about centre of mass - can be ignored
Important to check file globbing and sorting - depends on naming convention
'''

import sys, glob, re, os
import vtk
import pyvista as pv
import numpy as np

def GetStepFromFileName(fileString):
	return re.findall(r'(\d+.\d+).vtu', os.path.split(fileString)[1])[0]
	#return int(re.findall(r'(\d+)[.vtu]', os.path.split(fileString)[1])[0])

def getSurfacesInSac(surface,sac):
	enclosed = surface.select_enclosed_points(sac)
	enclosed.set_active_scalars('SelectedPoints') 
	enclosed = enclosed.threshold(0.5)
	return enclosed

def lines_from_points(points):
    """
    From pyvista tutorial https://docs.pyvista.org/examples/00-load/create-spline.html?highlight=polyline
    Given an array of points, make a line set
    """
    poly = pv.PolyData()
    poly.points = points
    cells = np.full((len(points)-1, 3), 2, dtype=np.int_)
    cells[:, 1] = np.arange(0, len(points)-1, dtype=np.int_)
    cells[:, 2] = np.arange(1, len(points), dtype=np.int_)
    poly.lines = cells
    return poly

def find_point_on_plane(r,theta,plane_center,orth1,orth2):
	#x = r*np.sin(theta)
	#y = r*np.cos(theta)
	#z =  -1*((normal[0]*x + normal[1]*y)/normal[2])

	#plane_orth_vector = np.array([x,y,z])


	#plane_orth_vector /= np.linalg.norm(plane_orth_vector)

	point = plane_center + r*np.cos(theta)*orth1 + r*np.sin(theta)*orth2

	#x += plane_center[0]
	#y += plane_center[1]
	#z += plane_center[2]

	return point[0],point[1],point[2]

if __name__ == '__main__':

	#########################################################
	
	#case = 'c0004'
	#p_id = 'P0116'
	#path_to_isos = '/Users/Lucas/Documents/quarantineV	iz/combined/ICA/qisos/sac_fullvolume/'

	case = 'c0020'
	p_id = 'P0238'
	path_to_isos = '/home/bsl/Documents/Lucas/aneurisk/q-iso/c0020/q=0.05/'

	#case = 'c0032'
	#p_id = 'P0088'
	#path_to_isos = '/home/lucas/Documents/viz/data/q_isosurfaces/c0032/sac_full_volume_0p05thresh/'

	#case = 'c0050'
	#p_id = 'P0147'
	#path_to_isos = '/home/bsl/Documents/Lucas/aneurisk/q-iso/c0050/q=0.33/'

	#case = 'c0053'
	#p_id = 'P0155'
	#path_to_isos = '/home/bsl/Documents/Lucas/aneurisk/q-iso/c0053/q_isosurface_0p5thresh_volume/'

	#case = 'c0054'
	#p_id = 'P0161'
	#path_to_isos = '/home/bsl/Documents/Lucas/aneurisk/q-iso/c0054/q=0.05/'

	#case = 'c0060'
	#p_id = 'P0177'
	#path_to_isos = '/home/bsl/Documents/Lucas/aneurisk/q-iso/c0060/q=0.05/'
	
	#case = 'c0068'
	#p_id = 'P0211'
	#path_to_isos = '/home/bsl/Documents/Lucas/aneurisk/q-iso/c0068/q=0.025/'

	####################################################################

	outdir = f'/home/bsl/Documents/Lucas/aneurisk/q-iso/{case}/flat/'

	sac_path = f'/home/bsl/Documents/Lucas/aneurisk/sac_geos/Aneurisk_SacData/{p_id}_sac.vtp'
	neck_plane_path = f'/home/bsl/Documents/Lucas/aneurisk/sac_geos/Aneurisk_SacData/{p_id}_firstclosedsection.vtp'

	##########################################################################




	q_isosurface_paths = sorted(glob.glob(path_to_isos+'/*.vtu'), key = GetStepFromFileName)

	sac = pv.read(sac_path)
	neck_plane = pv.read(neck_plane_path)
	neck_plane.compute_normals(inplace=True)

	normal = neck_plane['Normals'][0]

	projection_plane = sac.project_points_to_plane(origin = neck_plane.center, normal = normal)
	projection_plane.save(f'{outdir}/projection_plane.vtk')

	orth1 = (projection_plane.points[0] - projection_plane.center)
	orth1 /= np.linalg.norm(orth1)

	A,B,C = normal[0],normal[1],normal[2]
	D,E,F = orth1[0],orth1[1],orth1[2]

	o1 = 1
	o2 = (A - C*D/F)/(C*E/F-B)
	o3 = (A+B*o2)/(-1*C)

	orth2 = np.array([o1, o2, o3 ])
	orth2 /= np.linalg.norm(orth2)

	#point on plane and orthogonal to orth1 


	n_lines = 16
	#draw 16 radial lines from centre
	theta = np.linspace(0,2*np.pi,n_lines)
	r = 10

	master_sonification_q = np.zeros((n_lines,len(q_isosurface_paths)))
	master_sonification_r = np.zeros((n_lines,len(q_isosurface_paths)))

	for col,path in enumerate(q_isosurface_paths):
		print (f'Step {col} of {len(q_isosurface_paths)}  ... ', end = "\r")
		
		lines = pv.MultiBlock()
		centers = pv.MultiBlock()

		q = pv.read(path)
		q = getSurfacesInSac(q,sac)
		q = q.extract_surface()
		q = q.connectivity()

		if 'Q-criterion' in q.point_data.keys():

			q.set_active_scalars('Q-criterion')
			q_projection = q.project_points_to_plane(origin=neck_plane.center,normal=normal)


			for row,t in enumerate(theta):

				x1,y1,z1 = find_point_on_plane(r,t,projection_plane.center,orth1,orth2)

				x2,y2,z2 = find_point_on_plane(0.5,t,projection_plane.center,orth1,orth2)

				line_points = np.column_stack(([x2,x1],[y2,y1],[z2,z1]))  
				line = pv.Spline(line_points,2)#ines_from_points(line_points) 
				
				q_on_line = q_projection.slice_along_line(line)

				blob_center = q_on_line.center_of_mass()
				blob_radius = np.sqrt( (blob_center[0] - projection_plane.center[0])**2 + \
							  		   (blob_center[1] - projection_plane.center[1])**2 + \
							  		   (blob_center[2] - projection_plane.center[2])**2 )


				if q_on_line.GetNumberOfPoints() == 0:
					q_on_line_array = np.array([0,0,0,0,0])
				else:
					q_on_line_array = np.array(q_on_line.point_data['Q-criterion'])

				line.field_arrays['mean_q_on_line'] = np.mean(q_on_line_array)
				line.field_arrays['sum_q_on_line'] = np.sum(q_on_line_array)
				line.field_arrays['mean_q_on_line-isovalue'] = np.mean(q_on_line_array)-0.5
				line.field_arrays['distance_to_center'] = blob_radius
				line.field_arrays['theta'] = t
				
				lines.append(line)

				center_x,center_y,center_z = find_point_on_plane(blob_radius,t,projection_plane.center,orth1,orth2)

				centers.append(pv.PolyData(np.array([center_x,center_y,center_z])))

				q_sum = np.sum(q_on_line_array)
				if np.isnan(q_sum) == True:
					q_sum = 0
				if np.isnan(blob_radius) == True:
					blob_radius=9999
				master_sonification_q[row,col] = q_sum
				master_sonification_r[row,col] = blob_radius

		else:
			master_sonification_q[:,col] = 0
			master_sonification_r[:,col] = 100
			q_projection = pv.PolyData()
			x1,y1,z1 = 0,0,0
			x2,y2,z2 = 1,1,1
			line_points = np.column_stack(([x2,x1],[y2,y1],[z2,z1]))  
			line = pv.Spline(line_points,2)#ines_from_points(line_points) 
			lines.append(line)
			centers.append(pv.PolyData(np.array([0,0,0])))

		q_projection.save(f'{outdir}/flat_q_{str(GetStepFromFileName(path)).zfill(4)}.vtk')
		lines.save(f'{outdir}/lines_{str(GetStepFromFileName(path)).zfill(4)}.vtmb')
		centers.save(f'{outdir}/mass_center_{str(GetStepFromFileName(path)).zfill(4)}.vtmb')

			#p.add_mesh(line,color='black',line_width=2)
			#p.add_mesh(np.array(q_on_line.center))

	np.save(f'{outdir}/master_sonification_q.npy',master_sonification_q)
	np.save(f'{outdir}/master_sonification_r.npy',master_sonification_r)

		#p.show()
	

	#p = pv.Plotter() 
	#p.add_mesh(projection_plane,opacity=0.2)
	#p.add_mesh(line,color='black',opacity=0.2)    
	#p.add_mesh(q_projection,opacity=0.2)
	#p.add_mesh(q_projection.slice_along_line(line)) 

'''
	for path in q_isosurface_paths:

		q = pv.read(path)

		q = getSurfacesInSac(q,sac)
		q = q.extract_surface()
		q = q.connectivity()

		q.set_active_scalars('Q-criterion')
		q_projection = q.project_points_to_plane(origin=neck_plane.center,normal=normal)

		q_projection.points -= 0.01*normal

		q_projection.save(f'./c0053/flat_q/flat_q_{str(GetStepFromFileName(path)).zfill(4)}.vtk')

	#p = pv.Plotter()
	#p.add_mesh(projection_plane)
	#p.add_mesh(q_projection,scalars='Solution/u',clim = [0,1])

'''


