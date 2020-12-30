# BSL-sonification
Tools for sonification of BSL data, examples, documentation

Current state:
	test_sounds.py should render sound similar to ICAD 2020 submission - working on lab linux workstation.

To do (roughly temporal order):
	- documentation for preprocessing.py
	- finish other synthdefs - resynth, piched/noise only, chromagram, flat_q
	- Make a branch of BSL and document changes, eventually merge so these packages can work together
	- Argument specification for add_sound_to_video.py, and in general get all that working, w.r.t. path management, etc.
	- Utility to bulk compute flat q etc.
	- debugging tools
	- Clean and cross platform install instructions

Install  instructions (just taking notes so I can remember everything that has to be done):
	- pip install -e lib/supercollider/.  for sc library
	- synth class -> set synthdef path and sc path
	- choose sound device
	- handy.scd setup