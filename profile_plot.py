from grating_sim.profileMkr import makeProf
import matplotlib.pyplot as plt
from IPython import display
import numpy as np
import math
import warnings


def prof_plot(gType, profile, slope, depthF, nLayers, res, material, wavelength, period, path):
    if profile:
            img=makeProf(wavelength, period,slope,depthF,nLayers,res, material, gType, path)
            plt.figure(figsize=(12,4))
            
            ax=plt.gca()
            
            ax.set_ylabel(f"Depth = {depthF*wavelength*1000} nm")
            ax.set_xlabel(f"Period = {period*1000} nm")

            # Turn off tick labels
            ax.set_yticklabels([])
            ax.set_xticklabels([])
            ax.set_xticks([])
            ax.set_yticks([])
            legend=plt.legend(title = f"{material}", loc='lower left', frameon = False, title_fontsize='large')
            warnings.filterwarnings("ignore")
            plt.setp(legend.get_title(), color='white')
            plt.imshow(img, cmap='hot')
            display.display(plt.gcf())
