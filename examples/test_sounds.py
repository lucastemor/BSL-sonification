"""
Mostly for developement -- load a sample case and sonify using different techniques
Eventually this can become an example or useful for wrapping everything
"""

from sonify.synth_classes.python_synthdefs import Pxx_blob
from pathlib import Path
import numpy as np

if __name__ == '__main__':

	#load some data -- e.g., sac spectrogram
	data_path = Path('/home/lucas/Documents/BSL-sonification/data/aneurisk/spectrograms/c0053')

	Pxx_scaled = np.load(data_path.joinpath('sac_spectro.npy'))
	freqs = np.load(data_path.joinpath('freqs.npy'))
	bins = np.load(data_path.joinpath('bins.npy'))

	synth = Pxx_blob(Pxx_scaled,freqs,bins)
	synth.looptime = 10
	synth.send_spectro()
	synth.listen(path = 'test.wav')