import numpy as np

from clim_functions.datetime360 import *


def split_by_doy( data, datelist, DOY1 = [7, 1] ):
    """Rearranges data to be split by DOY1, which should be selected in summer (e.g. default July 1)
    to ensure winter months are consecutive for SSW counting
    Original code written by Michael Goss (bydntobydoy), adapted by Laura Mansfield 07/12/2021 for use
    with 360 day years (removed leap year needs, etc.) and translated into python 25/01/2022.
    Args: data: data array size [NY*360, ...] 
          datelist: vector of dates in datetime format (e.g. [[2000, 1, 1], [2000, 1, 2] , ... ])
          DOY1: Date of splitting the years, default [7, 1]
    Out:
        outdata: New data array that will be of size [NY+1, 360, ...] where NY is number of years in original data (padded with NaNs)
        yearlist: Years"""
    DPY = 360
    sz = data.shape
    ND = data.ndim     ## Note this only works for ND = 1
    
    # Convert datenumbers into datetimes using 360 day calendar
    yy = datelist[:, 0].copy()

    # Get days since DOY1 (so first half of year is -ve, second half is +ve, allowing us to split easily)
    doy1s = np.stack((yy, DOY1[0]*np.ones(len(yy)), DOY1[1]*np.ones(len(yy))), axis=-1)  
    days_since_doy = datenum360(datelist) - datenum360(doy1s)

    yy[days_since_doy < 1] = yy[days_since_doy < 1] - 1   # Move -ve values into previous 'year' (e.g. winter 2019 includes Jan/Feb of 2020)
    days_since_doy[days_since_doy < 1] = days_since_doy[days_since_doy < 1] + DPY 

    yearlist = np.arange(min(yy), max(yy)+1)
    NY = len(yearlist)
    padnanb = int(days_since_doy[0] )               # Pad with nans at begining
    padnane = int(DPY - days_since_doy[-1] - 1)     # Pad with nans at end
    
    # Add NaNs from DOY1 until Dec of year 1 and from Jan until DOY1 of last year
    padnanb_matrix = np.nan * np.ones((padnanb)) 
    padnane_matrix = np.nan * np.ones((padnane))
    outdata = np.concatenate((padnanb_matrix, data, padnane_matrix))
    
    # Reshape data to separate the years out
    outdata = np.reshape(outdata, (NY, DPY))  
    
    return(outdata, yearlist)
