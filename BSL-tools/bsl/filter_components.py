import h5py
from pathlib import Path
from shutil import copyfile
import numpy as np
from bsl import filters

input_path = Path('/Users/Lucas/Documents/AneurysmData/c0053_ACA/c0053_ACA_2500')
output_path = Path('/Users/Lucas/Documents/AneurysmData/c0053_ACA/c0053_ACA_LP_filtered25')
T =0.951

original_paths = list(input_path.glob('pipe_*.h5'))
n_steps = len(original_paths)
fs = n_steps/T
filtered_paths = [output_path.joinpath(Path(p).name) for p in original_paths]

#copy existing h5s so we can just resue xdmf etc.. dont ned it for now 
''' 
for i, original_step_path in enumerate(original_paths):
	print(f'Copying existing data ... Step {i} of {len(original_paths)}', end = "\r")
	copyfile(original_step_path, filtered_paths[i])
'''

print ('\n')

arbitrary_h5 = h5py.File(original_paths[0], 'r')
n_points = arbitrary_h5['Solution/u'][:].shape[0]
arbitrary_h5.close()


#initialize master_matricies - index by [poind_id, timetep, component]

np.save('unfiltered_component_matrix.npy',np.zeros([n_points, n_steps, 3]))
np.save('filtered_component_matrix.npy',np.zeros([n_points, n_steps, 3]))

unfiltered_component_matrix = np.load('unfiltered_component_matrix.npy',mmap_mode = 'r+')
filtered_component_matrix = np.load('filtered_component_matrix.npy',mmap_mode = 'r+')

#add to master matrix
for i,original_step_path in enumerate(original_paths):
	print (f"Consolidating timesteps into one matrix step {i+1} of {n_steps}...", end = "\r")
	original_h5 = h5py.File(original_step_path, 'r')
	unfiltered_component_matrix[:,i] = original_h5['Solution/u'][:]

	original_h5.close()

print ('\n')

#slice to get each component, filter each component
for component in [0,1,2]:
	print (f"Filtering component matricies ... Component {component+1} of 3", end = '\r')
	component_trace = unfiltered_component_matrix[:,:,component] #dimension: [n_points, n_steps]
	filtered_trace = filters.filter_time_data(component_trace,fs=fs,highcut=25,btype='lowpass')
	filtered_component_matrix[:,:,component] = filtered_trace

print ('\n')

#break up and write to h5s
for i,filtered_step_path in enumerate(filtered_paths):
	print (f"Writing to filtered h5s ... Step {i+1} of {n_steps}", end = "\r" )
	filtered_h5 = h5py.File(filtered_step_path, 'r+')
	filtered_h5['Solution/u'][:] = filtered_component_matrix[:,i]
	fil.close()
