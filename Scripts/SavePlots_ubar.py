### Example script to save ubar plots to file
### Run as main from parent directory
### python -m Scripts.SavePlots_ubar

import os
import glob
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

from plot_functions.plot_ubar import plot_ubar_seasonal , plot_ubar_annual, plot_ubar_daily
from plot_functions.make_gif import make_gif

# Select run to plot
run = '038'
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

print("Plotting...")
plot_ubar_annual(lat, pfull, ucomp, rundir)
print("Annual plot done")
plot_ubar_seasonal(lat, pfull, ucomp, rundir)
print("Seasonal plot done")
plot_ubar_daily(lat, pfull, ucomp, rundir, dday=15)
print("Daily plots done")
make_gif(rundir+'PLOTS/ubar_t')
print("Gif created")
