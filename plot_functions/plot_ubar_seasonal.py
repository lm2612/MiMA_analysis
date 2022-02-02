import numpy as np
import matplotlib.pyplot as plt

from plot_ubar import plot_ubar

from clim_functions.get_seasonal_inds import get_seasonal_inds 

def plot_ubar_seasonal(lat, pfull, ucomp, rundir=None):
    """ Plots 2x2 grid of zonal mean zonal winds for each season """
    n_days = (ucomp.shape)[0] 
    DJF_inds, MAM_inds, JJA_inds, SON_inds = get_seasonal_inds(n_days)
    nrows=2
    ncols=2
    
    plt.clf()
    fig, axs = plt.subplots(nrows, ncols,figsize=(8, 8), gridspec_kw = {'wspace':0.15, 'hspace':0.2}, sharey=True, sharex=True)
    axs = axs.flatten()
    # DJF
    plt.sca(axs[0])
    plot_ubar(lat[:], pfull[:], ucomp[DJF_inds].mean(axis=(0, 3)), title="DJF")
    # MAM
    plt.sca(axs[1])
    plot_ubar(lat[:], pfull[:], ucomp[MAM_inds].mean(axis=(0, 3)), title="MAM")
    # JJA 
    plt.sca(axs[2])
    plot_ubar(lat[:], pfull[:], ucomp[DJF_inds].mean(axis=(0, 3)), title="JJA")
    #SON
    plt.sca(axs[3])
    plot_ubar(lat[:], pfull[:], ucomp[DJF_inds].mean(axis=(0, 3)), title="SON")

    cbar_ax = fig.add_axes([0.1, 0.08, 0.8, 0.05])
    cbar = plt.colorbar(ticks=np.arange(-20, 20.5, 20), label='m/s',cax=cbar_ax,
                        orientation='horizontal')
    plt.subplots_adjust(bottom = 0.2)

    if rundir is not None:
        save_as = rundir+'PLOTS/ubar_seasonal.png'
        plt.savefig(save_as)
        print("Saved as ", save_as)
        plt.close()


