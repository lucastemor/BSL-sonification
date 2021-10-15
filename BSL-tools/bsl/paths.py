import re
from pathlib import Path 
'''
working only for aneurisk data right now
'''
base = Path.home().joinpath('Documents')

def case_data(case): #spectrograms
	dataPath = base.joinpath('AneurysmData','Aneurisk','spectrograms')
	dataPath = Path(list(dataPath.glob(f'*{case}*'))[0])
	return dataPath

def spectro(case):
	return case_data(case)
	#eturn case_data(case).joinpath('spectrograms')

def full_geo(case):
	return spectro(case).joinpath(f'{case}.vtu')

def transposed_matrix(case):
	return spectro(case).joinpath(f'{case}.h5')


def p_id_lookup(case):
	lookup_csv = base.joinpath('AneurysmData','Aneurisk','sac_geos','cases_vs_patient_ids.csv')
	for line in open(lookup_csv, 'r'):
		search = re.search(case.upper(), line)
		if search:
			p_id = re.findall('(P\d+)',search.string)[0]
			break
			if line == None:
				print ('no matches found')
	return p_id

def sac_geo(case, sac=False, neck_plane=False, aneurysm_surface=False):
	if sum([sac,neck_plane,aneurysm_surface])>1:
		print ('please specify one at a time')
		return 
	p_id = p_id_lookup(case)
	geos = base.joinpath('AneurysmData','Aneurisk','sac_geos','Aneurisk_SacData')
	if sac:
		return geos.joinpath(f'{p_id}_sac.vtp')
	if neck_plane:
		return geos.joinpath(f'{p_id}_firstclosedsection.vtp')
	if aneurysm_surface:
		return geos.joinpath(f'{p_id}_aneurysmsurface.vtp')

def getStepFromFileName(fileString):
	'''
	Parses time series file name and returns int timestep.  
	Assumes that the timestep is the last digit sequence in a file name before the extension
	eg., q_iso_thresh0p5__14.vtu will return 14 
	'''
	fpath = Path(fileString)
	return int(re.findall(r'(\d+)', fpath.stem)[-1])
