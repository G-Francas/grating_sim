from rcwa import Material
import grating_sim.context
import numpy as np
import matplotlib.pyplot as plt
import unittest
from grating_sim.shorthand import *
from grating_sim.matrices import *
from grating_sim.fresnel import *
from grating_sim.matrixParser import *
from grating_sim.source import Source
from grating_sim.layer import Layer
from grating_sim.solver import *
from grating_sim.crystal import Crystal
import cmath
import json
#Modules I've created
from grating_sim.slopecsv import Slopecsv
from grating_sim.newSlope import SlopeNew
from grating_sim.checkcsv import *
from grating_sim.profileMkr import makeProf
from grating_sim.profile_plot import prof_plot
from grating_sim.plot import plotter
from grating_sim.squarecsv import *
from grating_sim.Blazed import Blazedcsv
from grating_sim.polarization import *
def sim_setup(gType,depthF,slope,profile,wavelength,period,har,res,material,numLayer,theta,phi,pTEM, loop, path):
    tests=np.size(locals()[loop])
    loops=locals()[loop]
    depthFs=depthF
    slopes=slope
    wavelengths=wavelength
    periods=period
    hars=har
    ress=res
    numLayers = numLayer
    
    depthF=depthFs[0]
    slope=slopes[0]
    wavelength=wavelengths[0]
    period=periods[0]
    har=hars[0]
    res=ress[0]
    numLayer = numLayers[0]
    
    

    print(f"\nSimulating a {gType} diffraction grating made of {material}....")
   
    
    if material == 'Silicon':
        mat_name = 'Si'
    elif material == 'Aluminium':
        mat_name = 'Al'

    elif material == 'Silver':
        mat_name = 'Ag'

    elif material == 'Gold':
        mat_name = 'Au'

    elif material == 'Titanium':
        mat_name = 'Ti'

 

    #Creating basic layers
    
    reflectionLayer = Layer(er=1.0006, ur=1, L=10000)
    source = Source(wavelength=wavelength, theta=theta, phi=phi,pTEM=pTEM, layer=reflectionLayer)

    
    material_data = Material(mat_name)
    material_data.source = source
    er = material_data.er
    ur = 1
    baseLayer = Layer(er=er,ur=1, L=10000)

    print(f"Material permittivity er = {er}")
    
    if gType == 'Checkerboard':
        print("Creating layers for checkerboard simulation...\n")
        nLayers=Check(res,er, material, gType, path)
    if gType == 'Rectangular' and slope == 0:
        print("Creating layers for rectangular simulation with vertical sidewalls...\n")
        nLayers = Slopecsv(res,slope,depthF, material, gType, er, path)
        print(f'sim91 {path}')

    if gType == 'Square':
       print("Creating layers for square simulation...\n")
       nLayers=Square(res,er, material, gType, path) 
    if gType == 'CoatedChecker':
       print("Creating layers for coated checkerboard simulation...\n")
       nLayers=CheckCoat(res,er,material,gType, er_si, path)
    if gType == 'CheckerError':
        err=input("What percentage error would you like on the checkerboard? Please enter as a decimal, eg 0.3 for 30% error.")
        print(f"Creating layers for checkerboard simulation with error {err}...\n")
        nLayers=CheckErr(res,er, material, gType, err, path)
    if gType=='CheckDiag':
        print(f"Creating layers for checkerboard simulation on diagonal...\n")
        nLayers=CheckDiag(res,er,material,gType, path)
    if gType=='CheckDiagErr':
        err=input("What percentage error would you like on the checkerboard? Please enter as a decimal, eg 0.3 for 30% reduction in square size.")
        print(f"Creating layers for checkerboard simulation with error {err}...\n")
        nLayers=CheckDiagErr(res,er, material, gType, err, path)
    if gType=='Circ':
        print(f"Creating layers for circular grating simulation...\n")
        nLayers=Circ(res,er,material,gType, path)

    count=0
    
    depthF=depthFs.take([count],mode='clip')[0]
    
    slope=slopes.take([count],mode='clip')[0]
    wavelength=wavelengths.take([count],mode='clip')[0]
    period=periods.take([count],mode='clip')[0]
    har=hars.take([count],mode='clip')[0]
    res=ress.take([count],mode='clip')[0]
    numLayer=numLayers.take([count],mode='clip')[0]

    depth=depthF*wavelength
    #generate csv files
    if slope != 0:
        if gType=="Rectangular":
            print(f"Creating layers for rectangular grating with sloped sidewalls, slope={slope} degrees...\n")
            #nLayers = Slopecsv(res,slope,depthF, material, gType, er, path)
            nLayers = SlopeNew(res,slope,depthF, period, wavelength, material,numLayer, gType, er, path)

        elif gType == "Blazed":
            print(f"Creating layers for blazed grating of blaze angle {slope} degrees...\n")
            nLayers = Blazedcsv(res,slope,depthF, material, gType, er, path)
            
    else:
        if gType == 'Checkerboard':
            print("Creating layers for checkerboard simulation...\n")
            nLayers=Check(res,er, material, gType, path)
        if gType == 'Rectangular' and slope == 0:
            print("Creating layers for rectangular simulation with vertical sidewalls...\n")
            nLayers = Slopecsv(res,slope,depthF, material, gType, er, path)

        if gType == 'Square':
            print("Creating layers for square simulation...\n")
            nLayers=Square(res,er, material, gType, path) 
        if gType == 'CoatedChecker':
            print("Creating layers for coated checkerboard simulation...\n")
            nLayers=CheckCoat(res,er,material,gType, er_si, path)
        if gType == 'CheckerError':
            err=input("What percentage error would you like on the checkerboard? Please enter as a decimal, eg 0.3 for 30% error.")
            print(f"Creating layers for checkerboard simulation with error {err}...\n")
            nLayers=CheckErr(res,er, material, gType, err, path)
        if gType=='CheckDiag':
            print(f"Creating layers for checkerboard simulation on diagonal...\n")
            nLayers=CheckDiag(res,er,material,gType, path)
        if gType=='CheckDiagErr':
            err=input("What percentage error would you like on the checkerboard? Please enter as a decimal, eg 0.3 for 30% reduction in square size.")
            print(f"Creating layers for checkerboard simulation with error {err}...\n")
            nLayers=CheckDiagErr(res,er, material, gType, err, path)
        if gType=='Circ':
            print(f"Creating layers for circular grating simulation...\n")
            nLayers=Circ(res,er,material,gType, path)
    print("Profile: ")
    prof_plot(gType, profile, slope, depthF, nLayers, res, material, wavelength, period, path)