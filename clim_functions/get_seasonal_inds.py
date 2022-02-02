import numpy as np

def get_seasonal_inds(n_days):
    """ Returns 4 lists of indicies for DJF, MAM, JJA and SON to allow quick sub-selection
    over variables for each season. Assumes time series starts in Jan"""
    DJF = list(range(0, 60)) + list(range(330, 360))
    MAM = list(range(60, 150))
    JJA = list(range(150, 240))
    SON = list(range(240, 330))
    DJF_inds = [i for i in range(n_days) if i%360 in DJF]
    MAM_inds = [i for i in range(n_days) if i%360 in MAM]
    JJA_inds = [i for i in range(n_days) if i%360 in JJA]
    SON_inds = [i for i in range(n_days) if i%360 in SON]
    
    return DJF_inds, MAM_inds, JJA_inds, SON_inds
