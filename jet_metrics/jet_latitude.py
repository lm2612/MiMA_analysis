import os
import glob

import numpy as np
import netCDF4 as nc

from ..clim_functions import get_seasonal_inds

def jet_latitude(u, lat, eddy = False, return_SH_jet = False):
    """ Returns jet latitude timeseries """
    if eddy: 
        u_jet = ucomp[:, 36:39, :, :].mean(axis=(1,3))   # extract 850 hPa level (model levels 36-39 give 738 - 902 hPa) and take zonal mean

    else:
        u_jet = ucomp[:, 27:29, :, :].mean(axis=(1,3))   # extract 200 hPa level (model levels 27-29 give 194 - 231 hPa) and take zonal mean
    jet_lat = lat[32+np.argmax(u_jet[:, 32:], axis=1)]
    if return_SH_jet:
        jet_lat_SH = lat[np.argmax(u_jet[:, :32], axis=1)]
        return(jet_lat, jet_lat_SH)
    else:
        return(jet_lat)

def jet_latitude_means(jet_lat, return_variance = False, return_sd = False): 
    """ Returns jet lat mean and variance over entire time series. To get seasonal means, use (e.g.)
    DJF_inds, MAM_inds, JJA_inds, SON_inds = get_seasonal_inds(len(jet_lat))
    jet_lat_DJF = jet_latitude_means(jet_lat[DJF_inds]) """
    if return_variance:
        return jet_lat.mean(), jet_lat.var()
    elif return_sd:
        return jet_lat.mean(), jet_lat.std()
    else:
        return jet_lat.mean()

