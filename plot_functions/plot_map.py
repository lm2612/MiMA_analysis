import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point


def plot_map(lon, lat, variable, ax=None, title='', levels = None, color_bar = False):
    """ Plots map of variable, which must be of size len(lat) x len(lon). 
    This includes adding a cyclic point. You can provide an axis if you want it to be part
    of a subplot, but note ax must be a GeoAxes with a specified projection, e.g.
    fig, ax = plt.subplots(1, 1, figsize=(8, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    Optional title, levels and color_bar. If you want a color_bar, you must specify levels as
    these limits are used in the tickmarks. For more options you can turn this off and create
    a color bar separately at the end (e.g. for multiple subplots). """
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    
    ax.coastlines()
    plt.sca(ax)
    
    variable_cyclic, lons_cyclic = add_cyclic_point(variable, coord=lon)

    plt.contourf(lons_cyclic, lat[:], variable_cyclic, cmap = 'BrBG_r',
             levels = levels, extend='both')
    plt.title(title)
    if color_bar:
        cbar = plt.colorbar(ticks=np.arange(levels[0], levels[-1]+0.1, round(levels[-1] - levels[0])/4), 
                            location='bottom', label='m/s', orientation='horizontal')
    return ax


