import numpy as np
import matplotlib.pyplot as plt

def plot_ubar(lat, pfull, ubar, title='', levels = np.linspace(-40, 40, 100), color_bar = False):
    """ Plots zonal mean winds on latitude-pressure contour plot. ubar must be of dim len(pfull) x len(lat).
    e.g. ubar = np.mean(ucomp[t, :, :, :], axis=2) to take longitudinal avg, at time index t. 
    Set up plot axis before use. Title and levels optional. Can add color_bar (if single plot)
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
