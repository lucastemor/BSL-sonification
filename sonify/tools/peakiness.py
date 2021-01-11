import numpy as np
import matplotlib.pyplot as plt
import bsl.spectral
import scipy.signal
from pathlib import Path

def arc_length(x, y):
    """
    SOURCE: https://scicomp.stackexchange.com/questions/19384/calculate-contour-line-length
    """
    npts = len(x)
    arc = np.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)
    for k in range(1, npts):
        arc = arc + np.sqrt((x[k] - x[k-1])**2 + (y[k] - y[k-1])**2)

    return arc


def column_peakiness(spectra_column,bins):
    smoothed_column = scipy.signal.savgol_filter(spectra_column,31,3)
    spectra_length = arc_length(bins,spectra_column)
    smoothed_length = arc_length(bins,smoothed_column)
    return spectra_length/smoothed_length

def spectrogram_peakiness(spectrogram,bins):
	return np.apply_along_axis(column_peakiness,0,spectrogram,bins=bins)


if __name__ == '__main__':

	data_path = Path(f'/home/lucas/Documents/BSL-sonification/data/aneurisk/spectrograms/')
	outdir = Path('/home/lucas/Documents/AneurysmData/Aneurisk/peakiness')

	plot_scaling = 100
	peakiness_threshold = 2

	cases = data_path.glob('c*')

	for case in cases:
		name = case.stem

		pxx_path = data_path.joinpath(name,'sac_averaged')

		Pxx_scaled = np.load(pxx_path.joinpath(f'sac_spectro_unfiltered_scaled.npy'))
		freqs = np.load(pxx_path.joinpath(f'freqs.npy'))
		bins = np.load(pxx_path.joinpath(f'bins.npy'))

		peakiness_all_columns = spectrogram_peakiness(Pxx_scaled,bins)

		fig, ax = plt.subplots(3,1,figsize=(15,15))

		ax[0].pcolormesh(bins,freqs,Pxx_scaled,shading='gouraud')
		ax[0].plot(bins,peakiness_all_columns*plot_scaling,color='w',linewidth=3)
		ax[0].set_title(f'Case {name}: sac avg. spectrogram with {plot_scaling}x peakiness',fontsize=15)

		ax[1].plot(bins,peakiness_all_columns,linewidth=3)
		ax[1].set_ylim(0,10)
		ax[1].set_title('Peakness')

		ax[2].plot(bins,np.where(peakiness_all_columns>peakiness_threshold,peakiness_all_columns,0),linewidth=3)
		ax[2].set_ylim(0,10)
		ax[2].set_title(f'Threshhold peakiness > {peakiness_threshold}')

		plt.savefig(outdir.joinpath(f'{name}_peakiness.png'))
		plt.cla()
		plt.close()