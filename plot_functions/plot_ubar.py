"""Contains methods for plotting zonal mean winds on latitude pressure contour plots. Includes
annual, seasonal and daily plotting methods. """

import numpy as np
import matplotlib.pyplot as plt

from clim_functions.seasons import months, get_seasonal_inds

def plot_ubar(lat, pfull, ubar, title='', levels = np.linspace(-40, 40, 100), color_bar = False):
    """ Plots zonal mean winds on latitude-pressure contour plot. ubar must be of dimension
    len(pfull) x len(lat). e.g. ubar = np.mean(ucomp[t, :, :, :], axis=2) to take longitudinal 
    avg, at time index t.  Set up plot axis before use. Title and levels optional. Can add 
    color_bar (if single plot)
    Returns plot axis."""
    axs = plt.gca()

    plt.contourf(lat[:], pfull[:], ubar, cmap = 'BrBG_r', levels = levels, extend='both')
    plt.ylabel('Pressure (hPa)')
    plt.xlabel('Latitude')
    plt.xticks(np.arange(-90., 90.1, 30.))

    axs.set_yscale('log')
    axs.invert_yaxis()
    if color_bar:
        cbar = plt.colorbar(ticks=np.arange(-20, 20.5, 20), location='bottom', label='m/s',
                        orientation='horizontal')
    plt.title(title)
    return axs

def plot_ubar_annual(lat, pfull, ucomp, rundir=None):
    """ Plots annual zonal mean zonal winds """
    plt.clf()
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    plt.sca(ax)
    plot_ubar(lat[:], pfull[:], ucomp[:].mean(axis=(0, 3)), title="ANN", color_bar=True)
    plt.subplots_adjust(bottom = 0.2)

    if rundir is not None:
        save_as = rundir+'PLOTS/ubar_annual.png'
        plt.savefig(save_as)
        print("Saved as ", save_as)
        plt.close()
    return fig, ax
        
       
def plot_ubar_seasonal(lat, pfull, ucomp, rundir=None):
    """ Plots 2x2 grid of zonal mean zonal winds for each season """
    n_days = (ucomp.shape)[0] 
    DJF_inds, MAM_inds, JJA_inds, SON_inds = get_seasonal_inds(n_days)
    nrows=2
    ncols=2
    
    plt.clf()
    fig, axs = plt.subplots(nrows, ncols,figsize=(8, 8), 
                            gridspec_kw = {'wspace':0.15, 'hspace':0.2}, 
                            sharey=True, sharex=True)
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

    return fig, axs

        

def plot_ubar_daily(lat, pfull, ucomp, rundir, dday=1):
    """ Saves daily (or dday number of days) zonal mean zonal wind plots. Can be combined 
    with     gif_maker(...) to create animations. """
    ndays = ucomp.shape[0]
    for t in range(0, ndays, dday):
        plt.clf()
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        plt.sca(ax)
        day = t%30 + 1
        year = int(t/360) + 1
        month = months[int(t/30)%12]
        title = '{} {} {}'.format(day, month, year)
        plot_ubar(lat[:], pfull[:], ucomp[t, :, :, :].mean(axis=2), title=title, 
                  color_bar=True)
        
        save_as = rundir+'PLOTS/ubar_t={:04d}.png'.format(t)
        plt.savefig(save_as)
        print("Saved as ", save_as)
        plt.close()


        