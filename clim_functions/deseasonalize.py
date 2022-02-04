import numpy as np


def deseasonalize(variable, time):
    """Deseasonalize data, given time series of data. Monthly means over the 
    time series are computed and subtracted from the data.
    Arguments: variable, array of any size, as long as time is on axis 0. 
               time,     time vector which indicates which day corresponds 
               to the data variable. Must be same length as axis 0 of variable. 
    Returns variable_deseasonalized, array of same size as original variable 
               but with the mean of each month subtracted. """
    variable_deseasonalized = np.zeros(variable.shape)
    for i in range(12):
        # Get month indices
        month_i = list(range(i*30, (i+1) * 30))
        inds_month_i =  np.isin( time%360 , month_i )
        # Get variable data for this month
        variable_month = variable[inds_month_i]
        variable_month_mean = np.mean(variable_month)
        # Deseasonalize 
        variable_deseasonalized[inds_month_i] = variable_month - variable_month_mean
    return variable_deseasonalized