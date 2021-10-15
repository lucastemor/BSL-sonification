""" Example showing use of SpectrogramSampler()

SpectrogramSampler() inherits from DataSampler(), and is 
really just a plotting tool using PyVista. If you want to create 
a similar tool for a different purpose, reccomend checking 
out the source for SpectrogramSampler(), and creating a 
similar class.
"""

from pathlib import Path
import numpy as np 
import bsl
import pyvista as pv

# This example uses synthetic data. 
# But if you wanted, this is how you'd read in mesh file and data file
# mesh_file = ''
# np_file = ''
# mesh = bsl.io.read_mesh_data(mesh_file)
# df = np.load(np_file, mmap_mode='r')

T = 0.951
t = np.linspace(0,T,1250)

mesh = pv.Polygon()
mesh.points = mesh.points*10.0
ff = [0, 12, 123, 234, 345, 456]
df = np.array([0.1*np.sin((ff[idx])*2*np.pi*t/T) for idx in range(len(mesh.points))])

sp = bsl.sampling.SpectrogramSampler(df, mesh)
sp.sample_mode = 'all'
sp.create_plotter()
