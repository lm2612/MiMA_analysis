# Function to return period of QBO using FFT method
import numpy as np
import netCDF4 as nc
from scipy.fft import fft, fftfreq


def get_QBO_period_FFT(u_zonal):
    """ Function that returns the QBO period calculated using the FFT method.
    Inputs: u_mean (np array) zonal mean zonal wind, typical to use at 27hPa (MiMA index 17)
    Outputs: period (flt) period (period of peak power in fourier transformed zonal mean zonal wind at 27hPa)
             in years/months/days?
    """ 
    # Calculate period
    # Remove mean
    u_zonal_demean = u_zonal - np.mean(u_zonal, axis=0)
    # Increase spectral resolution by padding edges
    pad = np.zeros(u_zonal.shape)
    u_zonal_padded = np.concatenate((pad, u_zonal_demean, pad), axis=0)
    # fft
    power_spec = np.abs(fft(u_zonal_padded, axis=0))**2
    freqs = fftfreq(len(u_zonal_padded), 1/30)
    # find max
    max_ind = np.argmax(power_spec, axis=0)
    peak_freq = freqs[max_ind]
    period = 1/peak_freq

    return period 
