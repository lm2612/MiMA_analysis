### Example script to save ubar plots to file
### Run as main from parent directory
### python -m Scripts.SavePlots_ubar

import os
import glob
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from plot_functions.plot_ubar import plot_ubar_seasonal , plot_ubar_annual, plot_ubar_daily
from plot_functions.make_gif import make_gif

from clim_functions.mean_lat_weighted import mean_lat_weighted
from plot_functions.plot_map import plot_map


# Select run to plot
run = 'highres'
basedir = os.environ['SCRATCH']+'/MiMA/runs/'
rundir = basedir + run + '/'
print(rundir)

print(glob.glob(rundir+'*.nc'))
filename = 'atmos_daily'
dataset = nc.Dataset(rundir+filename+'.nc', 'r')

lon = dataset['lon']
lat = dataset['lat']
time = dataset['time']
pfull = dataset['pfull']
ucomp = dataset['ucomp']

# If plot folder does not exist, create one
if not os.path.exists(rundir+'PLOTS/'):
    os.makedirs(rundir+'PLOTS/')
    print('New dir created: '+rundir+'PLOTS/')

# Plot zonal means
print("Plotting...")
plot_ubar_annual(lat, pfull, ucomp, rundir)
print("Annual plot done")
plot_ubar_seasonal(lat, pfull, ucomp, rundir)
print("Seasonal plot done")
#plot_ubar_daily(lat, pfull, ucomp, rundir, dday=15)
#print("Daily plots done")
#make_gif(rundir+'PLOTS/ubar_t')
#print("Gif created")

# Plot QBO
# Plot contours of zonal mean wind speeds in 4degS-4degN region (inds 30-34)
u_zonal = mean_lat_weighted( ucomp[:, :, 30:34, :].mean(axis=(-1)), lat[30:34], axis=(-1) )
t = (time[:]-time[0])/360.

nrows = 1
ncols = 1

levels = np.linspace(-40, 40, 100)

plt.clf()
fig, axs = plt.subplots(nrows, ncols,figsize=(10, 6), gridspec_kw = {'wspace':0., 'hspace':0.}, sharey=True)

plt.contourf(t, pfull[:], u_zonal.T, 
                     cmap = 'BrBG_r', levels = levels, extend='both')
plt.ylabel('Pressure (hPa)')
plt.xlabel('Time (years)')
plt.xticks(np.arange(t[0], t[-1] ,1.))
axs.set_yscale('log')
axs.invert_yaxis()
cbar = plt.colorbar(ticks=np.arange(-20, 20.5, 20), location='bottom', label='m/s',
                            orientation='horizontal')

plt.savefig(rundir+'PLOTS/QBO_zonalmean_vs_time.png')

# Plot SSWs
# Extract zonal mean u at 10hPa, 60N (59.99702 - 62.787354)
model_level = 13
lat_level = 53
u10at60 = mean_lat_weighted(ucomp[:, model_level, 53:55, :].mean(axis=(-1)), 
                                    lat[53:55], axis=(-1) )    # Zonal mean

fig = plt.figure(figsize=(10, 6))
plt.plot(t, np.zeros(len(u10at60)), 'k--')
plt.plot(t, u10at60)
plt.xticks(np.arange(t[0], t[-1] ,1.))
plt.xlabel('Time (years)')
plt.ylabel('ubar at 10 hPa at 60degN')
plt.savefig(rundir+'PLOTS/SSW_ubar_10hPa_60N.png')


# Plot parameterized GW drag
gwfu_cgwd = dataset['gwfu_cgwd']
gwfv_cgwd = dataset['gwfv_cgwd']

model_level = 23
model_height = pfull[model_level]
gwd_u = gwfu_cgwd[:, model_level, :, :].mean(axis=0)
gwd_v = gwfv_cgwd[:, model_level, :, :].mean(axis=0)


nrows = 1
ncols = 2

levels = np.linspace(-2e-6, 2e-6, 100)

plt.clf()
fig, axs = plt.subplots(nrows, ncols,figsize=(16, 8), gridspec_kw = {'wspace':0.15, 'hspace':0.1},
                        subplot_kw={'projection': ccrs.PlateCarree()}, sharey=True)


plt.sca(axs[0])
plot_map(lon[:], lat[:], gwd_u, ax=axs[0], levels=levels, title='gwd u ({:.2g} hPa)'.format(model_height))
plt.sca(axs[1])
plot_map(lon[:], lat[:], gwd_v,  ax=axs[1], levels=levels, title='gwd v ({:.2g} hPa)'.format(model_height))
#cbar = plt.colorbar(ax=axs[1], ticks=[-1e-6, -5e-7, 0, 5e-7, 1e-6], location='right', label='m/s^2',
#                orientation='vertical')
plt.suptitle("Parameterized GW drag")
plt.savefig(rundir+'PLOTS/cgwd_lonlat_{:.2g}hPa.png'.format(model_height))



# Plot QBO drag
# Plot contours of zonal mean zonal drag in 4degS-4degN region (inds 30-34)
gwdu_zonal = mean_lat_weighted( gwfu_cgwd[:, :, 30:34, :].mean(axis=(-1)), lat[30:34], axis=(-1) )
levels = np.linspace(-5e-5, 5e-5, 100)
nrows = 1
ncols = 1
plt.clf()
fig, axs = plt.subplots(nrows, ncols,figsize=(10, 6), gridspec_kw = {'wspace':0., 'hspace':0.}, sharey=True)
plt.contourf(t, pfull[:], gwdu_zonal.T,  cmap = 'BrBG_r', levels = levels, extend='both')
plt.ylabel('Pressure (hPa)')
plt.xlabel('Time (years)')
plt.xticks(np.arange(t[0], t[-1] ,1.))

axs.set_yscale('log')
axs.invert_yaxis()
cbar = plt.colorbar(ticks=np.arange(-5e-5, 5.01e-5, 1e-5), location='bottom', label='m/s^2',orientation='horizontal')
plt.suptitle("Parameterized zonal GW drag for QBO")
plt.savefig(rundir+'PLOTS/QBO_cgwd.png')


# Plot SSW drag
# Plot contours of zonal mean wind speeds in 60N region (inds 53:55)
gwdu_zonal = mean_lat_weighted( gwfu_cgwd[:, :, 53:55, :].mean(axis=(-1)), lat[53:55], axis=(-1) )
levels = np.linspace(-1e-5, 1e-5, 100)

nrows = 1
ncols = 1
plt.clf()
fig, axs = plt.subplots(nrows, ncols,figsize=(10, 6), gridspec_kw = {'wspace':0., 'hspace':0.}, sharey=True)
plt.contourf(t, pfull[:], gwdu_zonal.T,
             cmap = 'BrBG_r', levels = levels, extend='both')
plt.ylabel('Pressure (hPa)')
plt.xlabel('Time (years)')
plt.xticks(np.arange(t[0], t[-1] ,1.))

axs.set_yscale('log')
axs.invert_yaxis()
cbar = plt.colorbar(ticks=np.arange(-1e-5, 1.01e-5, 5e-6), location='bottom', label='m/s^2',orientation='horizontal')
plt.suptitle("Parameterized zonal GW drag for SSW")
plt.savefig(rundir+'PLOTS/SSW_cgwd.png')
print("Plotted GW drag")


 

