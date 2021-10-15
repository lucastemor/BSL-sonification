""" Sample data within mesh using a sphere as probe.

This example shows how to use the bsl.sampling.DataSampler class.
DataSampler is instantiated with a mesh (N points), and a
"dataframe" (an array-like structure, shape N by M timesteps).
By specifying a probe, points from the mesh will be sampled.
"""

from pathlib import Path
import numpy as np 
import bsl
import pyvista as pv
import matplotlib.pyplot as plt

# For this example, specify your mesh (N points) and the array-like 
# "dataframe" file. This file should have shape (N rows, M timesteps). 

# Here's how you might load read data:
# mesh_file = ''
# np_file = ''
# mesh = bsl.io.read_mesh_data(mesh_file)
# df = np.load(np_file, mmap_mode='r')

# But we'll use synthetic data instead.
# Here, we make polygon with 6 points. We create a synthetic 
# data array, df, by creating a sinusoid associated with
# each point in the polygon.
T = 0.951
t = np.linspace(0,T,1250)

mesh = pv.Polygon()
mesh.points = mesh.points*10.0
ff = [0, 12, 123, 234, 345, 456]
df = np.array([0.1*np.sin((ff[idx])*2*np.pi*t/T) for idx in range(len(mesh.points))])

# Create a probe centered at one of the mesh points.
probe = pv.Sphere(radius=15.0, center=mesh.points[3])

# Create the data sampler and set params.
ds = bsl.sampling.DataSampler(df, mesh)
ds.sample_mode = 'all'
ds.set_probe(probe)
ds.generate_sample_ids()
ds.sample_data()

ds.plot()

_, _, fs = bsl.spectral.get_sampling_constants(df, T=0.951)

df_sampled = ds.df_sampled

Pxx_ave, freqs, bins = bsl.spectral.compute_spectrogram(
    df=df_sampled, 
    fs=fs,
    )

plt.pcolormesh(bins, freqs, Pxx_ave, shading='gouraud')
plt.show()