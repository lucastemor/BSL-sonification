""" High-pass filter time data using Butterworth filter
"""
import numpy as np
import bsl
import matplotlib.pyplot as plt 

mesh_file = ''
np_file = ''

# Specify sampling frequency 
fs = 1250

# Create a time axis
t = np.linspace(0,1,fs)

# Create a low-frequency "carrier" and high-frequency "fluctuation"
x1 = np.sin(np.pi*t)
x2 = 0.2*np.sin(25*2*np.pi*t)

x = x1 + x2

plt.plot(t, x)

# Typically, we might have N points to filter, in an
# array of shape (N, M timesteps). Here, we need to 
# reshape our array x so that it has shape (1, 1250)
x = x.reshape(1, -1)

# Isolate the high-frequency flucuation
x_high = bsl.filters.filter_time_data(
    x, 
    fs=fs, 
    lowcut=10, 
    btype='highpass',
    )

# Isolate the low-frequency carrier
x_low = bsl.filters.filter_time_data(
    x, 
    fs=fs, 
    highcut=10, 
    btype='lowpass',
    )

# When we plot, we use index = 0 to specify the first point.
plt.plot(t, x[0], label='True', linewidth=3)
plt.plot(t, x_high[0], label='High')
plt.plot(t, x_low[0], label='Low')
plt.plot(t, x_high[0] + x_low[0], label='Low+High', linestyle='--')
plt.legend()
plt.show()