# Function to return QBO period using Transition Time method
import numpy as np
import netCDF4 as nc
from scipy.ndimage import uniform_filter1d
from clim_functions.smoothing import smooth

def get_QBO_TT(u_zonal, return_variance=False, return_amplitude=False, return_cov=False):
    """ Function that returns QBO period using Transition Time (TT) method 
    Inputs: u_zonal (np array) zonal mean zonal wind at given height level, recommended 10hPa (MiMA index 13) 
    Outputs: period (flt) mean period in months 
             amplitude (flt)  absolute max. u within each QBO cycle"""
    # Smooth with five-month centered running mean
    u_smoothed = smooth(u_zonal)

    # Identify zero wind transitions from westward to eastward (i.e. -ve to +ve)
    # Note, we start in the +ve phase, so calculate no of QBOs from then
    new_QBO_cycle = []
    t = range(len(u_zonal))
    # Go through time series and save each transition
    for it in t[1:]:
        if (u_smoothed[it] >=0 and u_smoothed[it-1] <= 0):
            new_QBO_cycle.append(it)
                   

    print("QBO transition times:", new_QBO_cycle)
    new_QBO_cycle = np.array(new_QBO_cycle)
    periods = new_QBO_cycle[1:] - new_QBO_cycle[:-1]
    periods_mon = periods/30.
    
    # Calculate mean period
    mean_period = np.mean(periods_mon)
    
    if return_amplitude:
        amplitudes = np.zeros(len(periods))
        for ic in range(len(periods)):
            start_ind = new_QBO_cycle[ic]
            end_ind = new_QBO_cycle[ic+1]
            amplitudes[ic] = 0.5 * (np.max(u_smoothed[start_ind:end_ind] ) - 
                                    np.min(u_smoothed[start_ind:end_ind] ) )

        # Calculate mean amplitude
        mean_amplitude = np.mean(amplitudes)
        
        # And covariance or variance if required
        if return_cov:
            cov = np.cov(periods_mon, amplitudes)
            return mean_period, mean_amplitude, cov
        elif return_variance:
            var_amplitude = np.var(amplitudes)
            var_period = np.var(periods_mon)
            return mean_period, mean_amplitude, var_period, var_amplitude
        else:
            return mean_period, mean_amplitude

    elif return_variance:
        var_period = np.var(periods_mon)
        return mean_period, var_period
    else:
        return mean_period

    
