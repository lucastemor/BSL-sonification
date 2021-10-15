""" Utilities for filtering temporal signals 
"""
import numpy as np
from scipy.signal import butter, lfilter, filtfilt, windows, istft


def butter_bandpass(fs, lowcut=None, highcut=None, order=5, btype='band'):
    """ Generate filter coefficients for Butterworth filter

    Parameters
    ----------
    fs : float  
        Sampling frequency (samples per second)  
    lowcut : float  
        Lower cutoff frequency. Higher frequencies pass through  
    highcut : float  
        Higher cutoff frequency. Lower frequencies pass through  
    order : int, optional  
        Order of the Butterworth filter  
    btype : str, optional  
        Filter type. Options: 'band', 'highpass', 'lowpass'  

    Returns
    -------
    b, a : array  
        Numerator (b) and denominator (a) polynomials of the IIR filter  

    Notes
    -----
    To actually *filter* the data, see butter_bandpass_filter
    If bytpe: 'highpass' selected, 'highcut' is not used
    lowcut = cutoff frequency for low cut
    highcut = cutoff frequency for high cut
    fs is samples per second
    returns filter coeff for butter_bandpass_filter function
    See SciPy docs for more info.
    """
    nyq = 0.5 * fs
    if (btype == 'band') or (btype == 'highpass'):
        low = lowcut / nyq
    if (btype == 'band') or (btype == 'lowpass'):
        high = highcut / nyq

    if btype == 'band':
        b, a = butter(order, [low, high], btype='band')
    elif btype == 'highpass':
        b, a = butter(order, low, btype='highpass')
    elif btype == 'lowpass':
        b, a = butter(order, high, btype='lowpass')
    return b, a 

def butter_bandpass_filter(data, fs, lowcut=None, highcut=None, order=5, btype='band'):
    """ Filter a 1D array with a Butterworth filter
    
    Parameters
    ----------
    data : array (1D)  
        Array to be filtered  
    fs : float  
        Sampling frequency of data  
    lowcut : float  
        Lower cutoff frequency. Higher frequencies pass through  
    highcut : float  
        Higher cutoff frequency. Lower frequencies pass through  
    order : int, optional  
        Order of the Butterworth filter  
    btype : str, optional  
        Filter type. Options: 'band', 'highpass', 'lowpass'  

    Returns
    -------
    y : array (1D)  
        Filtered data array  
    """
    b, a = butter_bandpass(fs, lowcut, highcut, order=order, btype=btype)
    y = filtfilt(b, a, data)
    return y

def filter_time_data(data, fs, lowcut=None, highcut=None, order=6, btype='highpass'):
    """ Convenience function for filtering each row in a 2D array

    Parameters
    ----------
    See butter_bandpass_filter for descriptions  

    Returns
    -------
    array  
        Filtered data array  

    """
    
    data_filt = data.copy()
    for idx, row in enumerate(np.array(data)):
        data_filt[idx] = butter_bandpass_filter(
            row,
            fs = fs,
            lowcut = lowcut,
            highcut = highcut,
            order = order, 
            btype = btype,
            )

    return data_filt

def apply_window(data, tukeyalpha=1.0):
    """ Window a 1D data array 

    Parameters
    ----------
    data : array, shape (N points, M timesteps)    
        Array of data  

    Returns
    -------
    array   
        Windowed data array  
    """
    data_windowed = data.copy()
    wlength = len(data_windowed[0])

    for idx, row in enumerate(data):
        data_windowed[idx] = row*windows.tukey(wlength, alpha=tukeyalpha)
        
    return data_windowed
