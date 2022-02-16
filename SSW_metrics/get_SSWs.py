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


def get_consec_counts(vec):
    """ Counts number of consecutive days that vector is in a particular state 
    (e.g. winds are below a threshold, vec is the vector of indices that satisfy 
    this threshold).
    Args: vec = np array of indices that satifies the condition for given state. This
                should be obtained using np.argwhere(CONDITION).
    Returns: counts = np array of number of consecutive days 
             start_inds     = np array of indices when the condition flips to true.
    """
    vec = vec.reshape(-1)
    nanvec = np.array([np.nan])
    
    # Get starting ind when new conditions is satisfied
    start_vec = np.concatenate( (nanvec, vec) )
    start_inds = np.argwhere(start_vec[1:] - start_vec[:-1]!=1).reshape(-1)

    # Get ending inds when this condition is no longer satisfied
    end_vec = np.concatenate( (vec, nanvec))
    end_inds = np.argwhere(end_vec[:-1] - end_vec[1:]!=-1).reshape(-1)

    # Count number of days the condition is satisfied for
    counts = end_inds - start_inds + 1
    
    return (counts, start_inds)

def get_SSWs(u10at60, datelist):
    """ Get SSWs 
    Args: u10at60 np array of mean zonal winds at 10 hPa, 60 degN
          datelist list of dates, e.g. createyear360(len(u10at60), 2000)
     """
        
    ## Constants
    USSWTHRESH = 0         # Threshold of u for sudden stratospheric warming
    USPVTHRESH = 48        # Threshold of u for strong polar vortex
    MINCONSECS = 20        # Min. number of consecutive days 
    INITWESTERLIES = 10    # Number of consecutive days to say the season for SSWs has started (polar vortex formed)
    FINALEASTERLIES = 10   # Number of consecutive days to say the season for SSWs has finished (final warming occurred)
    
    # Separate year so that winter runs consecutive
    doy_data, yearlist = split_by_doy(u10at60, datelist)
    datenum = datenum360(datelist)
    doy_dates, _ = split_by_doy(datenum, datelist)
    
    # Get SSWs
    pv_init_dates = []
    final_warming_dates = []
    ssw_dates = []
    spv_dates = []
    pvactive_dates = []
    ssw_count = 0
    for yi in np.arange(1,len(yearlist)-1):
        cyr = yearlist[yi]
        print(yi, " YEAR: ", cyr)
        cdata = doy_data[yi, :]
        cdates = doy_dates[yi, :]

        ### Check for zonal mean wind speed conditions
        # Get inds where data is sub and sup u SSW threshold (u=0)
        sub_ssw_inds = np.argwhere(cdata < USSWTHRESH)  
        sup_ssw_inds = np.argwhere(cdata >= USSWTHRESH)
        # Get starting inds and counts no. of consecutive days
        sub_ssw_consecs, sub_ssw_start = get_consec_counts(sub_ssw_inds)    
        sup_ssw_consecs, sup_ssw_start = get_consec_counts(sup_ssw_inds)

        #### Get initial and final dates of the SSW season
        # Find first date where us are westerly for at least INITWESTERLIES days
        first_sup_ssw = np.argwhere(sup_ssw_consecs >= INITWESTERLIES).reshape(-1)[0]
        pv_init_i = sup_ssw_inds[sup_ssw_start[first_sup_ssw]].squeeze()
        # Find final warming date where us are easterly for at least FINALEASTERLIES days
        final_sup_ssw = np.argwhere(sup_ssw_consecs >= FINALEASTERLIES).reshape(-1)[-1]
        final_warming_i = sub_ssw_inds[sub_ssw_start[final_sup_ssw+1]].squeeze()
        # All SSW events must occur between pv_init_i and final_warming_i
        print("PV init on day ", pv_init_i, ". Final warming on day ", final_warming_i)

        #### Count number of times SSW conditions are met
        for pci in range(1, len(sup_ssw_consecs)):
            start_n = sub_ssw_inds[sub_ssw_start[pci]].squeeze()     # Date of start of negative winds, (cni in MG code)
            start_p = sup_ssw_inds[sup_ssw_start[pci]].squeeze()     # Date of return to positive, (cpi in MG code)
            prev_p = sup_ssw_inds[sup_ssw_start[pci-1]].squeeze()    # Date of previous positive ind, (ppi in MG code)
            if start_n>pv_init_i and start_n<final_warming_i and start_n-prev_p>=MINCONSECS and final_warming_i-start_p >= MINCONSECS:
                print("!!! SSW !!! on day", start_n, ". Days after previous +ve wind: " , start_n-prev_p, ". Days until final warming:", final_warming_i-prev_p)
                ssw_count += 1
                datenum_ssw = cdates[start_n]
                ssw_dates.append(datenum_ssw)

        #### Check for Strong Polar Vortex conditions
        # Get inds where data is sub and sup SPV threshold (u=48m/s)
        sub_spv_inds = np.argwhere(cdata <= USPVTHRESH)  
        sup_spv_inds = np.argwhere(cdata > USPVTHRESH)
        # Get starting inds and counts no. of consecutive days
        sub_spv_consecs, sub_spv_start = get_consec_counts(sub_spv_inds)    
        sup_spv_consecs, sup_spv_start = get_consec_counts(sup_spv_inds)
        
        #### Count number of times SPV conditions are met
        if (len(sub_spv_consecs)>=1):
            for pci in range(len(sub_spv_consecs)-1):
                start_p = sup_spv_inds[sup_spv_start[pci]].squeeze()     # Date of start of positive SPV ind (cpi in MG code)
                start_n = sub_spv_inds[sub_spv_start[pci]].squeeze()     # Date of start of negative SPV ind (cni in MG code)
                if ( start_p >= pv_init_i ) and ( start_p - start_n >= MINCONSECS ):
                    print(""" SPV SATISFIED""")
                    datenum_spv = cdates[start_p]
                    spv_dates.append(datenum_spv)
          
    return ssw_dates, spv_dates
