import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy import signal


def lp_filter(u, n_months=4):
    """ Removes high freq. variability with Butterworth low-pass filter, 9th order, cutoff 120 days (4 months) """
    n_days = n_months*30    # default 4 month
    sos = signal.butter(N=9, Wn=1/n_days, btype='low', output='sos')
    u_filtered = signal.sosfilt(sos, u, axis=0)
    return u_filtered

def smooth(u, n_months=5):
    """ Smooth with five-month centered running mean """
    n_days = n_months*30     # default 5 month
    u_smoothed = uniform_filter1d(u, n_days, axis=0)
    return u_smoothed
