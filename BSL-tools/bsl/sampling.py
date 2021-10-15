""" Utilities for sampling mesh data using a probe mesh.
"""

from pathlib import Path
import pyvista as pv
import bsl
import numpy as np 
from sklearn.neighbors import KDTree 
from pyvistaqt import BackgroundPlotter

class DataSampler():
    """ Spatially sample data by specifying an ROI

    Attributes
    ----------
    df : array, size (N_points, M_timesteps)  
        An array or dataframe containing data to be sampled (eg velocity)  
    mesh : PyVista vtkUnstructuredGrid   
        A volume mesh containing the corresponding N points  
    sample_ids : array  
        Array of pt IDs generated from generate_sample_ids  
    sample_density : float, in range [0,1]  
        The sampling density per unit volume  
    sample_mode : str, options: ['random_sample', 'all']  
        Random_sample samples from a uniform point cloud. All returns all  
        points within the probed location  
    sample_points : PolyData  
        PolyData of points corresponding to sample_ids  

    Methods
    -------
    set_probe(probe_mesh)  
        Set the mesh used to probe the data  
    generate_sample_ids()  
        Extract sample IDs according to the above attributes  
    sample_data()  
        Slice the array df using the ids generated from generate_sample_ids()  
    plot()  
        After generate_sample_ids, plot the mesh and the sampled points  

    """
    def __init__(self, df, mesh):
        self.df = df
        self.mesh = mesh
        self.sample_ids = [0]
        self.sample_density = 0.1
        self.sample_mode = 'all'

        _, _, self.fs = bsl.spectral.get_sampling_constants(self.df, T=0.951)

        self.surface = mesh.extract_surface().fill_holes(50.0) 
        self.surface.compute_normals(inplace=True)
        self.create_kdtree()

    def set_probe(self, probe_mesh):
        self.probe = probe_mesh 

    def generate_sample_ids(self):
        """ Extracts IDs within probe corresponding to points on the mesh """

        if self.sample_mode == 'all':
            mask = self.probe
            selection = self.mesh.select_enclosed_points(self.probe)
            mask_index = selection.point_arrays['SelectedPoints']
            ids = [x for x in range(len(selection.points)) if mask_index[x] == True]
                    
        elif self.sample_mode == 'random_sample':
            point_cloud = bsl.common.random_sample_mesh(
                self.probe, self.probe.bounds, self.sample_density)
            selection = point_cloud.select_enclosed_points(self.surface)
            mask_index = selection.point_arrays['SelectedPoints']
            mask_index = [x for x in range(len(selection.points)) if mask_index[x] == True]
            ids = bsl.common.get_ID_of_nearest_points(point_cloud.points[mask_index], self.tree)

        if len(ids) == 0: ids = [0]
        self.sample_points = pv.PolyData(self.mesh.points[ids])
        self.sample_ids = ids

    def sample_data(self):
        """ Sample  main array by slicing using sample_ids as index"""
        self.df_sampled = self.df[self.sample_ids] 

    def create_kdtree(self):
        """ Creates a kdtree for random sampling"""
        self.tree = KDTree(self.mesh.points, leaf_size=2)

    def plot(self):
        p = pv.Plotter()
        p.add_mesh(self.surface, opacity=0.1)
        p.add_mesh(self.probe, opacity=0.1)
        p.add_mesh(self.sample_points)
        p.show()

class SpectrogramSampler(DataSampler):
    """ Sample spectrogram using interactive probe

    Attributes
    ----------
    Pxx_ave : array, 2D  
        Spectrogram array  
    freqs : array, 1D  
        Freuencies returned from spectrogram generation  
    bins : array, 1D  
        Time bins returned from spectrogram generation  

    Methods
    -------
    create_plotter()   
        Creates an interactive plotter for choosing location  
    get_local_spectrogram()  
        Called by create_plotter(). Generates and stores   
        Pxx_ave, freqs, bins as attributes.  

    Notes
    -----
    This is just an example of how to create an interactive probe. For other 
    uses, or other plotting requirements, create a new class, inhereit 
    DataSampler, and follow the logic set herein.
    """
    def __init__(self, df, mesh):
        DataSampler.__init__(self, df, mesh)

    def get_local_spectrogram(self):
        """ Computes the average spectrogram from the generated sample IDs"""
        self.sample_data()
        Pxx_ave, freqs, bins = bsl.spectral.compute_spectrogram(
            self.df_sampled, 
            self.fs,
            )

        self.Pxx_ave = Pxx_ave
        self.freqs = freqs
        self.bins = bins
    
    def create_plotter(self):
        """ Create a PyVista plotter for interactively probing and sampling
        
        Notes
        -----
        Creates a PyVista background plotter for interactively sampling 
        df based on locations in mesh. Note, this interactivity is not 
        necessary for simply sampling or computing spectra.
        """
        self.p = BackgroundPlotter(shape="1|1", window_size=(800,500))

        self.p.subplot(0)
        self.p.add_mesh(self.surface, opacity=0.1)

        # # Initialize IDs for spectrogram plot; sample point 0 in mesh
        self.sample_points = pv.PolyData(self.mesh.points[self.sample_ids])
        self.pts_actor = self.p.add_mesh(self.sample_points)
        self.p.add_slider_widget(callback=self.slider_callback, rng=(0.,10.), value=0.5, title = 'Sample Density')

        self.get_local_spectrogram()
        self.grid = bsl.common.convert_array_to_uniform_grid(self.Pxx_ave.T, 'Pxx')

        self.p.subplot(1)
        self.pxx_actor = self.p.add_mesh(self.grid) 

        # Add probe
        self.p.subplot(0)
        self.p.add_sphere_widget(
            callback=self.probe_callback, 
            style='wireframe', 
            theta_resolution=8, 
            phi_resolution=8,
            pass_widget=True,
            center=self.mesh.points[0]
            )

        self.p.view_xy()
        self.p.disable()


    def slider_callback(self, value):
        self.sample_density = value

    def probe_callback(self, xyz, probe):
        """ Callback function for sphere widget in create_plotter """
        print('xyz', xyz, 'rad', probe.GetRadius())

        self.probe = pv.Sphere(radius=probe.GetRadius(), center=probe.GetCenter()) 
        self.generate_sample_ids()

        if len(self.sample_ids) > 0:
            self.get_local_spectrogram()

            self.p.subplot(0)
            self.p.remove_actor(self.pts_actor)
            self.pts_actor = self.p.add_mesh(self.sample_points, reset_camera=False)

            self.p.subplot(1)
            self.grid.point_arrays['Pxx'] = self.Pxx_ave.flatten()
            self.p.remove_actor(self.pxx_actor)
            self.pxx_actor = self.p.add_mesh(self.grid, reset_camera=False) 

if __name__ == "__main__":
    data_folder = Path('/Volumes/storage/research_data/data_spectrogram/')
    data_file = sorted(data_folder.glob('c*/c*.h5'))[0]
    mesh_file = sorted(data_folder.glob('c*/c*.vtu'))[0]

    mesh = bsl.io.read_mesh_data(mesh_file)

    # df = bsl.io.read_pd_dataframe(data_file)

    np_file = data_file.parent / (data_file.name + '.npy')
    # np.save(np_file, np.array(df))

    df = np.load(np_file, mmap_mode='r')

    dd = DataSampler(df, mesh)

    # data_object = SpectrogramSampler(df, mesh)
    # data_object.create_plotter()

    # data_object.p.show()