import numpy as np
import matplotlib.pyplot as plt

from plot_ubar import plot_ubar

from clim_functions.months import months

def plot_ubar_daily(lat, pfull, ucomp, rundir, dday=1):
    """ Plots daily (or dday number of days) zonal mean zonal winds and saves them. Can be used to create gifs. """
    ndays = ucomp.shape[0]
    for t in range(0, ndays, dday):
        plt.clf()
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        plt.sca(ax)
        day = t%30 + 1
        year = int(t/360) + 1
        month = months[int(t/30)%12]
        title = '{} {} {}'.format(day, month, year)
        plot_ubar(lat[:], pfull[:], ucomp[t, :, :, :].mean(axis=2), title=title, color_bar=True)
        
        save_as = rundir+'PLOTS/ubar_t={:04d}.png'.format(t)
        plt.savefig(save_as)
        print("Saved as ", save_as)
        plt.close()

