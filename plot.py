from grating_sim.profileMkr import makeProf
import matplotlib.pyplot as plt
from IPython import display
import numpy as np
import math


def plotter(firstxs,firstys,zeros,diags,R,loop, gType, tests,count, profile, slope, depthF, nLayers, res, material, wavelength, period, har,val,path):
    
    modes=np.linspace(-int(har/2),int(har/2), num=har)
    angles=np.arcsin(modes*wavelength/period)    
    plt.figure()
    plt.scatter(180*angles/math.pi,R[int(har/2),:])
    plt.title(f"Efficiency of reflected modes at different angles. {loop}={val}")
    plt.ylabel('Efficiency')
    plt.xlabel('Angle (degrees)')
    display.display(plt.gcf())
    
    
    efficiency=np.append(R[int(har/2),:], R[:,int(har/2)])
    xs=np.append(10*np.tan(angles), np.zeros(np.shape(angles)))
    ys=np.append(np.zeros(np.shape(angles)), 10*np.tan(angles))
    
    plt.figure()
    plt.scatter(xs,ys,s=efficiency*10000, c=efficiency,cmap='autumn')
    plt.colorbar(label='efficiency')
    plt.title("Diffracted mode positions 1cm above grating")
    plt.ylabel("y direction position in mm ")
    plt.xlabel("x direction position in mm")
    display.display(plt.gcf())


    
    if profile:
        img=makeProf(wavelength, period,slope,depthF,nLayers,res, material, gType, path)
        plt.figure(figsize=(12,4))
        
        ax=plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.xlabel(f"Period = {period} nm")
        plt.ylabel(f"Depth = {depthF*wavelength} nm")

        plt.imshow(img)
        display.display(plt.gcf())
    return 
    
    
