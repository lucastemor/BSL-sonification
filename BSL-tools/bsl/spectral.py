""" Utilities for generating spectrograms from time data.
"""

import numpy as np
from scipy.signal import spectrogram
from bsl import filters 
import matplotlib.pyplot as plt

def get_sampling_constants(df, T=0.951):
    """ Convience function for generating common sampling constants  
  
    Parameters  
    ----------  
    df : array or dataframe  
        Array of data, size [number of points, number of tsteps]  
    T : float, optional  
        Period of data, seconds. Usually 0.951s in BSL   
  
    Returns  
    -------  
    T : float  
        Period of data, seconds. Usually 0.951s in BSL   
    nsamples : int  
        Number of time samples in df  
    fs : float  
        Sample rate in samples per second  
    """
    nsamples = df.shape[1]
    fs = nsamples/T 
    return T, nsamples, fs 

def shift_bit_length(x):
    """ Round up to nearest pwr of 2  
  
    Parameters  
    ----------  
    x : int  
  
    Returns  
    -------  
    int  
        Nearest power of 2 to x, rounded up  
  
    Notes  
    -----  
    See https://stackoverflow.com/questions/14267555/  
    find-the-smallest-power-of-2-greater-than-n-in-python  
    """
    return 1<<(x-1).bit_length()

def get_spectrogram(x, fs, scaling='spectrum', mode='psd', overlap=0.75, wlength='default'):
    """ Calculates spectrogram for a single trace  
    
    Parameters  
    ----------  
    x : array, 1D  
        Data array to generate spectrogram from  
    fs : float  
        Dampling frequency of the data  
    scaling : str  
        Scaling mode for spectrogram. Options: ['density', 'spectrum']  
    mode : str  
        Defines return values. Options are [‘psd’, ‘complex’,   
        ‘magnitude’, ‘angle’, ‘phase’]  
    overlap : float, range [0, 1]  
        Percent overlap of subsequent windows  
    wlength : int  
        Window length given by number of samples  
    
    Returns  
    -------  
    Pxx : array, 2D  
        Power spectrum (or phase, mag, etc) generated from spectra  
    freqs : array, 1D  
        Frequency bins for Pxx  
    bins : array, 1D  
        Time bins for Pxx  
    
    Notes  
    -----  
    See scipy.signal.spectrogram docs  
    """  

    # wlength ->  length of window; here, 1/10th of total signal length
    if wlength == 'default':
        wlength = shift_bit_length(int(len(x)/10))
    else:
        try:
            wlength = int(wlength)
        except ValueError:
            "Invalid wlength, should be integer number of timesteps"


    freqs, bins, Pxx = spectrogram(
        x,
        fs = fs,
        nperseg = wlength,
        noverlap = int(overlap*wlength),
        nfft = wlength, # Adds zero padding
        window = 'hann',
        scaling = scaling,
        ) 
    
    Pxx[Pxx<=0] = 1e-16
    return Pxx, freqs, bins

def get_average_spectrogram(data, fs, scaling='spectrum', mode='psd', overlap=0.75, wlength='default'):
    """ Convenience function for generating an average spectrogram  

    Parameters  
    ----------  
    See "get_spectrogram" for parameter inputs  
    
    Returns  
    -------  
    Pxx : array, 2D  
        Mean of all power specta  
    Pxx_var : array, 2D  
        Variance of all power spectra  
    freqs : array, 1D  
        Frequency bins for Pxx  
    bins : array, 1D  
        Time bins for Pxx  
    """
    for idx, row in enumerate(np.array(data)):
        Pxx, freqs, bins = get_spectrogram(
            x=row, 
            fs=fs, 
            scaling=scaling, 
            mode=mode,
            overlap=overlap,
            wlength=wlength,
            )
        if idx == 0:
            Pxx_ave = Pxx
            Pxx_var = np.zeros(Pxx.shape)
        else:
            # Note, also calculating running variance
            # See https://math.stackexchange.com/
            # questions/20593/calculate-variance-from-a-stream-of-sample-values

            Pxx_ave_prev = Pxx_ave
            Pxx_ave = Pxx_ave + (Pxx - Pxx_ave)/(idx+1) # (k+1) because 0 idx
            Pxx_var = Pxx_var + (Pxx - Pxx_ave_prev)*(Pxx - Pxx_ave)

    return Pxx_ave, Pxx_var/(idx), freqs, bins

def spectrogram_scaling(Pxx, lower_thresh = -30.0):
    """ Log scale and threshold spectrograms for viewing or proessing 
    
    Parameters  
    ----------  
    Pxx : array, 2D  
        Power spectrum (or phase, mag, etc) generated from spectra  
    lower_threshold : float, optional  
        Lower threshold in decibels  
    
    Returns  
    -------  
    Pxx_scaled  
        Scaled and thresholded spectrogram  
    """  
    Pxx_scaled = np.log(Pxx)
    Pxx_threshold_indices = Pxx_scaled < lower_thresh
    Pxx_scaled[Pxx_threshold_indices] = lower_thresh
    return Pxx_scaled

def compute_spectrogram(df, fs, scaling='spectrum', mode='psd', overlap=0.75, wlength='default'):
    """ Compute a 'conventional' average spectrogram with pre-filtering

    Parameters  
    ----------  
    df : array, 2D  
        Array of data, size [number of points, number of tsteps]  
    fs : float  
        Sampling rate of data  
    For remaining params, see 'get_spectrogram'  
    
    Returns  
    -------  
    Pxx_ave : array, 2D  
        Mean spectrogram for the given data  
    freqs : array, 1D  
        Frequency bins for Pxx  
    bins : array, 1D  
        Time bins for Pxx  

    Notes  
    -----  
    This is a convenience function intended to generate a 'conventional' 
    spectrogram for typical data (1 cardiac cycle of velocity data, N points). 
    If you want to play more with filtering, or if your data is significantly 
    different than typical (much lower fs, <1 cycle, constant velocity), 
    double check any parameters in the get_spectrogram function.  
    """

    df_filtered = filters.filter_time_data(
        np.array(df), 
        fs=fs, 
        lowcut=25, 
        btype='highpass',
        )

    df_filtered = filters.apply_window(df_filtered, tukeyalpha=0.5)

    Pxx_ave, Pxx_var, freqs, bins = get_average_spectrogram(
        data=df_filtered, 
        fs=fs, 
        scaling='spectrum', 
        mode='psd', 
        overlap=0.75, 
        wlength='default',
        )

    Pxx_ave = spectrogram_scaling(Pxx_ave)

    return Pxx_ave, freqs, bins

def plot_spectrogram(bins,freqs,Pxx,case_name,path=None):
    plt.figure()
    plt.pcolormesh(bins, freqs, Pxx, shading = 'gouraud')

    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.xlim([0,0.951])
    plt.title('Case {}'.format(case_name))

    xx, yy = np.meshgrid(bins,freqs)
    plt.scatter(xx,yy, s=2, c='k', alpha=0.05)

    if path != None:
        print (path)
        plt.savefig(path)

def fft_tool():
    """ FFT of 1D data  
    Not implemented  
    """
    pass