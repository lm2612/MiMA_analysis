import numpy as np
import matplotlib.pyplot as plt

from plot_ubar import plot_ubar

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


