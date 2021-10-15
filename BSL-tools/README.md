# BSL tools

A collection of tools and utilities for processing spatiotemporal data.

Link to [documentation](https://biomedical-simulation-lab.github.io/BSL-tools/docs/bsl/index.html).

## Dependancies
For this repo, PyVista is heavily used as a replacement for VTK. For the purposes of everyday prototyping, this bridge between VTK's extensive library and NumPy-style funcationality is incredibly useful.

- meshio 
- scipy 
- numpy 
- pyvista and pyvistaqt
- scikit-learn
- pandas (optional)

In the lab, we've experiemented with formatting data using pandas, hdf5, and numpy. It seems numpy memory-mapped arrays are the best performing when you need access to all timesteps, so I'll be moving to that paradigm. To load an `npy` array in memory-mapped mode, simply use `np.load(npy_file, mmap_mode='r')`.

## Install
To install, clone this repo to your machine. `cd` into the folder, then enter `pip install .`. 

You should then be able to use these utilities in any project in your environment using `import bsl`.

## How to contribute
If you want to add or modify this repo: 
 
- First, use `pip install -e .` to install. The -e flag indicates development mode -- changes to the package are automatically included without reinstalling.
- Try to maintain the documentation patterns (based on the NumPy spec). This helps with autodocumenting the code. 
- Note to self: generate docs with pdoc --html --overwrite --html-dir docs bsl

## Notes on maintenance
- Docs are generated using `pdoc`. 
- See https://stackoverflow.com/questions/19048732/python-setup-py-develop-vs-install 
- Also https://timothybramlett.com/How_to_create_a_Python_Package_with___init__py.html