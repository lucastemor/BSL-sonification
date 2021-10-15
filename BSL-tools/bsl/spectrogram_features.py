import numpy as np 
from scipy.signal import find_peaks, peak_prominences
#import cv2 as cv


def get_envelope(Pxx,freqs):
	'''
	How I've been extracting envelope. Results in 'clipping' 
	'''
	thresh = np.where(Pxx>Pxx.min(),0,1)

	envelope = np.zeros(Pxx.shape[1])
	maxF = Pxx.shape[0]-1

	for idx, column in enumerate(thresh.T):
	    if column.max()>0:
	        height = maxF-np.nonzero(column)[0][0]
	        envelope[idx] = freqs[height]

	return(-1*envelope+freqs.max()) #flip 




def get_bands_and_extrapolation(Pxx,freqs,height=0.75,width=2, abs_zero=-20,return_coeffs=False):
	'''
	Given spectrogram matrix (eg., 129x36) will look at each time bin in the spectrogram trace and find peaks reletive the the baseline falloff of power
	peak height and width can be tuned if more bands/less bands are being extracted than what is visually perceived
	The default values above seem to work reasonably well for dB scaled spectrograms
	absolute zero point depends on spectrogram scaling -- so if it is db scaled, the oint of 0 power is -20 db .. etc .. 
	'''

	relativePeakHeight = np.zeros_like(Pxx)
	extrapolated_envelope = np.zeros(Pxx.shape[1])

	line_coeffs = [(0,0) for _ in range(Pxx.shape[1])]

	for time_bin in range (0, Pxx.shape[1]):
		col = Pxx.T[time_bin]
		peaks, _ = find_peaks(col)

		if len(peaks)>0:
			_,lb,rb = peak_prominences(col,peaks)
			troughs = np.unique(np.concatenate((lb,rb),0))
			
			falloff_line=[]

			for j in range(1,len(troughs)-1): #find local minima - ignore first peak @ ~25 Hz
				current_minima = troughs[j]
				prev_minima = troughs[j-1]
				next_minima = troughs[j+1]

				if col[current_minima]> col[next_minima] and col[current_minima]<col[prev_minima]:
					falloff_line.append(current_minima)

			if falloff_line == []:
				falloff_line = [0]

			interp = np.interp(freqs,freqs[falloff_line],col[falloff_line])
			

			floor = np.where(col-interp>0,col-interp,0)
			peaks,properties = find_peaks(floor,height=height,width=width) #,width=2)

			if len(peaks)<2: #so we don't extract just one peak - assuming that we want to extract periodic banded structures and not single peaks
				peaks=[]

			####the four lines below are new, they will fit a line to falloff points and find the freq where it hits -20db
			if np.unique(interp).shape[0] > 1:
				slope, intercept = np.polyfit(freqs[falloff_line],col[falloff_line],1) 
				neg_20db_point = (abs_zero-intercept)/slope
				extrapolated_envelope[time_bin] = neg_20db_point
				line_coeffs[time_bin] = (slope,intercept)

			relativePeakHeight.T[time_bin][peaks] = properties['peak_heights']

		else:
			floor = col-col #i.e, we have no peaks and only broadband falloff

		'''
		plt.figure()
		plt.plot(freqs,col,label = 'original')
		plt.hlines(-20,0,neg_20db_point+200,label = '-20 dB')
		x = np.linspace(0,neg_20db_point,10)
		plt.plot(x,x*slope+intercept)
		'''

		mask = np.isin(col,col[peaks])
		binary = np.where(mask==True, 1,0)

		col = col*binary
		Pxx.T[time_bin] = col

		#relativePeakHeight.T[time_bin][peaks] = properties['peak_heights'] #moved into if statement

	if return_coeffs:
		return Pxx,relativePeakHeight,extrapolated_envelope, line_coeffs
	else:
		return Pxx,relativePeakHeight,extrapolated_envelope


def extrapolated_spectrogram(trace,freqs):
	'''
	Given single trace, interpolate line, find 0 point
	'''
	plt.figure()
	plt.plot(freqs,trace)






