""" Commmon mesh-processing and generation utilities  
"""
import vtk
import numpy as np 
import h5py
import meshio
import pyvista as pv
from scipy.ndimage.morphology import distance_transform_edt 
from pathlib import Path
from sklearn.neighbors import KDTree 

def extract_surface(unstructured_grid):
    """ Extract surface from VTK unstructured grid
    
    Parameters
    ----------
    unstructured_grid : vtkUnstructuredGrid  
        Unstructured grid object  

    Returns
    -------
    vtkPolyData  
        Surface of unstructured_grid  
    """
    surf_extract = vtk.vtkGeometryFilter()
    surf_extract.SetInputData(unstructured_grid)
    surf_extract.Update()
    return surf_extract.GetOutput()

def meshio_cells_to_pv_cells(cells):
    """ Convert meshio "cells" array to PyVista "faces" format
    
    Parameters
    ----------
    cells: array  
        Cell connections from a meshio mesh  

    Returns
    -------
    array  
        Foramtted array for use with PyVista conventions  

    Notes
    -----
    PyVista (VTK) allows cells to be different shapes, eg you could
    have a triangle and quad in same mesh. 
    The first "column" in a PyVista faces array should indicate the number of 
    verts in that cell. 
    Here, meshes are all triangles, so stack in a column of 3s.
    """

    cells_tri = np.zeros(cells[0][1].shape[0], dtype=np.int) + 3
    cells_pv = np.concatenate([cells_tri.reshape(-1,1), cells[0][1]], axis=1)
    cells_pv = np.hstack(cells_pv)
    return cells_pv


def resample_to_image(obj, spacing, bounds=None, cushion=5):
    """ Resample any object to image, including associated arrays 

    Parameters
    ----------
    obj : PolyData, UnstrucutredGrid, UniformGrid, etc  
        Object to be resampled onto a uniform grid  
    spacing : array, length 3  
        The resolution of the returned voxel image  
    
    Returns
    -------
    PyVista Uniform Grid (vtkImageData)  
        The resampled object  
    """
    if bounds is None:
        bounds = np.array(obj.bounds)
        bounds[::2] -= cushion
        bounds[1::2] += cushion

    grid = create_grid(bounds, spacing)
    surf = obj.extract_surface().fill_holes(50.0) 
    surf.compute_normals(inplace=True)

    grid = grid.sample(obj)

    clipped = surf.clip_box(bounds, invert=False).extract_surface()

    grid.compute_implicit_distance(clipped, inplace=True)
    grid.rename_array('vtkValidPointMask', 'mask')
    grid.point_arrays['mask'] = grid.point_arrays['mask']*1.0
    return grid

def get_volume_of_bounds(bounds):
    """ Calculate the volume of the given bounds

    Parameters
    ----------
    bounds : array  
        Formatted vtk style  

    Returns
    -------
    volume : float  
        Volume of bounds  
    """
    bounds = np.array(bounds)
    lengths = bounds[1::2] - bounds[::2]
    return np.prod(lengths)

def random_sample_mesh(surface, bounds, sample_density):
    """ Generate spatially random uniform points within a surface

    Parameters
    ----------
    surface : vtkPolyData  
        A closed surface that we want to sample  
    bounds : array  
        Bounds within we would like to sample. Formatted VTK style  
    sample_density : float  
        The density of the rand uniform point cloud per unit volume  

    Returns
    -------
    vtkPolyData  
        PolyData contains random points within the surface  
    """
    point_cloud = random_uniform_point_cloud(bounds, sample_density)
    mask = point_cloud.select_enclosed_points(surface) 
    mask_index = mask.point_arrays['SelectedPoints']
    mask_index = [x for x in range(len(mask.points)) if mask_index[x] == True]
    mask = pv.PolyData(mask.points[mask_index])
    return mask

def get_ID_of_nearest_points(xyzpoints, tree=None, mesh=None):
    """ Given xyz coordinate(s), return ID of nearest vert in tree

    Parameters
    ----------
    xyzpoints : array, shape (N_points, 3)  
        Point or list of points used to find nearest vertex in mesh.  
    tree : KDTree, optional  
        Tree returned from KDTree(mesh.points, leaf_size=2). 
        See sklearn KDTree.  
    mesh : object having attribute .points, eg pv PolyData, optional  
        The object used to create the the tree  

    Returns
    -------
    ind : list  
        The list of indices of mesh that are nearest to xyzpoints  

    Notes
    -----
    Either tree or mesh must be given. Supplying tree is preferable  
    so that tree need not be recreated with each query.  
    """
    if tree is None:
        if mesh is None:
            raise RuntimeError('Either tree or mesh must be given')
        tree = KDTree(mesh.points, leaf_size=2)
    if xyzpoints.shape[0] != 0:
        dist, ind = tree.query(xyzpoints, k=1)  
        ind = sorted(ind.flatten())
    else:
        ind = []
    return np.unique(ind)

def random_uniform_point_cloud(bounds, density):
    """ Create a random uniform point cloud of given density and bounds

    Parameters
    ----------
    bounds : array  
        Bounds of the generated point cloud. Formatted VTK style  
    density : float  
        The density of the rand uniform point cloud per unit volume  
        eg if mesh is in mm, sample_density = 1 means 1 sample per mm^3  

    Returns
    -------
    vtkPolyData  
        A random uniform point cloud laying within the given bounds  
    """
    volume = get_volume_of_bounds(bounds)
    num_samples = int(volume * density)
    mins = np.array(bounds[0::2])
    maxs = np.array(bounds[1::2])
    points = np.random.random((num_samples, 3))
    points = (points * (maxs - mins)) + mins
    point_cloud = pv.PolyData(points)
    return point_cloud

def create_bounds(center, extent):
    """ Create an array in VTK bounds format with given center and extent
    
    Parameters  
    ----------  
    center : array  
        A point xyz indicating the center of the bounds  
    extent : array   
        The length of each side of the bounding box   

    Returns  
    -------
    array  
        VTK formatted bounds array  
    """
    ROI_lower = list(center - extent/2)
    ROI_upper = list(center + extent/2)
    ROI_bounds = ROI_lower + ROI_lower
    ROI_bounds[::2] = ROI_lower
    ROI_bounds[1::2] = ROI_upper
    return ROI_bounds

def create_grid(bounds, spacing):
    """ Create a uniform grid with given bounds and spacing

    Parameters
    ----------
    bounds : array  
        Bounds of grid, formatted VTK style  
    spacing : array  
        xyz spacing of uniform grid  

    Returns
    -------
    PyVista UniformGrid  
        Uniform grid with given bounds and spacing  
    """
    spacing = np.array(spacing)

    origin = bounds[::2]
    bounds = np.array(bounds).reshape(3,2)
    bbox_lens = bounds[:,1] - bounds[:,0]

    dimensions = np.array(bbox_lens/spacing, dtype=int) + 1

    image = pv.UniformGrid()
    image.dimensions = dimensions
    image.spacing = spacing
    image.origin = origin

    return image

def calc_signed_distance_image(mask_img):
    """ Calculate the distance to background (0) for non-zero points in array
    
    Parameters
    ----------
    mask_img : array  
        Image array with background values of 0  
  
    Returns  
    -------  
    array  
        Element-wise distance from background  
    """
    distance = distance_transform_edt(mask_img)
    return distance 

def convert_array_to_uniform_grid(array, name, spacing = 'squish'):
    """ Convert array to uniform grid
    """

    if len(array.shape) < 3:
        array = array[..., np.newaxis]

    grid = pv.UniformGrid()
    if spacing == 'squish':
        grid.spacing = [1/array.shape[0], 1/array.shape[1], 1]

    grid.dimensions = [array.shape[0], array.shape[1], 1]
    grid.point_arrays[name] = array.flatten(order="F")
    return grid




