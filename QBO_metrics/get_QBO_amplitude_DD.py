# Function to return 3 QBO metrics given an array
import numpy as np
import netCDF4 as nc

from clim_functions.smoothing import lp_filter

def get_QBO_amplitude_DD(u_zonal):
    """ Returns vertical amplitude of QBO using DD method
    Inputs: u_mean (np array) zonal mean zonal wind at 20hPa (MiMA index 16) or 77hPa (MiMA index 22)
    
    Outputs: amplitude (flt) vertical amplitude at given height level estimated as sqrt(2)*stdev after applying 
    a low-pass 9th order Butterworth filter is applied with 120 day cutoff to remove high frequency variability 
    """
    
    # Remove high freq. variability with low-pass filter, 9th order, cutoff 120 days
    u_filtered = lp_filter(u_zonal)
    # Calculate amplitude metrics
    stdev = np.std(u_filtered, axis=0)
    # Multiply by sqrt 2
    amplitude = np.sqrt(2) * stdev

    return amplitude

