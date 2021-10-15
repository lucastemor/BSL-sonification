"""
Utilities for reading and writing various files.
"""

import vtk
import meshio 
from pathlib import Path
import pyvista as pv 

from bsl import common

def read_mesh_data(filename, ext=None):
    """ Read a mesh file

    Parameters
    ----------
    filename : str  
        Path to file  
    ext : str, optional  
        File extension to use  

    Returns
    -------
    if file is not .vtu : vtkPolyData  
    if file is .vtu : vtkUnstructuredGrid  
        Defers to vtkUnstructuredGridReader for vtu. Meshio   
        has trouble with .vtu files.   

    Notes
    -----
    Need to include readers for xdmf, h5, etc.
    """
    
    ext = Path(filename).suffix.split('.')[1]
    file = Path(filename)

    if ext in ['h5', 'hdf5']:
        raise NotImplementedError('Need to write readers for h5 and hdf5')

    if ext not in ['vtu']:
        mesh = meshio.read(file, ext)

        # Convert mesh to PyVista polydata
        points = mesh.points
        cells_pv = common.meshio_cells_to_pv_cells(mesh.cells)
        return pv.PolyData(points, cells_pv)

    else:
        # print('Warning: returnextracting surface from vtu')
        mesh = ReadPolyData(file)
        return pv.UnstructuredGrid(mesh)

def read_pd_dataframe(filename):
    import pandas as pd 
    """ Convenience function for loading pandas hdf dataframe
    
    Parameters
    ----------
    filename : Path to file  

    Returns
    -------
    dataframe   
        Dataframe is loaded into memory.  
    """
    print('Loading dataframe. This may take a moment.')
    return pd.read_hdf(filename)

def read_xdmf_to_array(file, vector_name, stride = 1, num_cycles = 2, last_cycle = True):
    """ Read all timesteps from xdmf file into a numpy array
    
    Parameters
    ----------
    file: str  
        xdmf file  
    vector_name : str  
        From oasis, default "Assigned Vector Function"  
    stride: int, optional  
        Take every Nth timestep  

    Returns
    -------
    mesh  
        MeshIO mesh  
    vector_data  
        returned vector, shape (num tsteps, num pts, num dimensions)  
    tsteps  
        tstep indicies read  

    Notes
    -----
    This is probably specific to Dan's 2D XDMF files at the moment. 
    Need to make more general.
    TODO: for now, last_cycle is always true. Consider allowing all cycles. 
    TODO: more generally, only save the last cycles in Oasis
    """

    with meshio.xdmf.TimeSeriesReader(file) as reader:
        points, cells = reader.read_points_cells()
        z_points = np.zeros(points.shape[0])
        points = np.concatenate([points, z_points.reshape(-1,1)], axis=1)
        mesh = meshio.Mesh(points, cells)
        
        t_last = int(reader.num_steps - reader.num_steps/num_cycles)
        tsteps = list(range(t_last, reader.num_steps))[::stride]

        vector_data = np.zeros((len(tsteps), points.shape[0], points.shape[1]))

        for idx, k in enumerate(tsteps):
            t, point_data, cell_data = reader.read_data(k)
            vector_data[idx] = point_data[vector_name]

    return mesh, vector_data, tsteps


def ReadPolyData(filename):
    """Load the given file, and return a vtkPolyData object for it.  
    From ASLAK'S common tools.  
    """

    # Check if file exists
    if not filename.exists():
        raise RuntimeError("Could not find file: %s" % filename)

    # Check filename format
    fileType = filename.suffix[1:]
    if fileType == '':
        raise RuntimeError('The file does not have an extension')

    # Get reader
    if fileType == 'stl':
        reader = vtk.vtkSTLReader()
        reader.MergingOn()
    elif fileType == 'vtk':
        reader = vtk.vtkPolyDataReader()
    elif fileType == 'vtp':
        reader = vtk.vtkXMLPolyDataReader()
    elif fileType == 'vtu':
        reader = vtk.vtkXMLUnstructuredGridReader()
    elif fileType == "vti":
        reader = vtk.vtkXMLImageDataReader()
    else:
        raise RuntimeError('Unknown file type %s' % fileType)

    # Read
    reader.SetFileName(str(filename))
    reader.Update()
    polyData = reader.GetOutput()

    return polyData

def WritePolyData(input_data, filename):
    """Write the given input data based on the file name extension  
    From ASLAK'S common tools.  
    """
    # Check filename format
    fileType = filename.split(".")[-1]
    if fileType == '':
        raise RuntimeError('The file does not have an extension')

    # Get writer
    if fileType == 'stl':
        writer = vtk.vtkSTLWriter()
    elif fileType == 'vtk':
        writer = vtk.vtkPolyDataWriter()
    elif fileType == 'vtp':
        writer = vtk.vtkXMLPolyDataWriter()
    elif fileType == 'vtu':
        writer = vtk.vtkXMLUnstructuredGridWriter()
    else:
        raise RuntimeError('Unknown file type %s' % fileType)

    # Set filename and input
    writer.SetFileName(filename)
    if version < 6:
        writer.SetInput(input_data)
    else:
        writer.SetInputData(input_data)
    writer.Update()

    # Write
    writer.Write()
