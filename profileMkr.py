# -*- coding: utf-8 -*-
"""profile.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14rUtsFFQaJ40HthS20E-PAJuxnlPJps3
"""

import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

import math
from IPython.display import Image as Mirage

import sys

def upScale(arr, scaleFactor):
    bigArr = np.zeros(np.size(arr)*scaleFactor)
    place=0
    for i in arr:
        repeat=0
        while repeat < scaleFactor:
            bigArr[place+repeat] = i
            repeat+= 1
        place += scaleFactor
    return bigArr



def makeProf(wavelength, period, theta, depthF, nLayers,res, material, gType, path):
  nm= 10**(-9)
  um=10**(-6)
  n=0


  depth = depthF*wavelength
  dres = int(res*depth/period)
  resOG = res       
  
  
  rowPLayer = dres/nLayers
  scaleFac=1
  if rowPLayer < 1:
        dres = dres*100
        res = res*100
        scaleFac = 100
        rowPLayer = int(rowPLayer*100)
  elif rowPLayer < 10:
        dres = dres*10
        res = res*10
        scaleFac=10
        rowPLayer = int(rowPLayer*10)
  rowPLayer = int(rowPLayer)
  profA=np.zeros((2*dres,res))     
  place=0
  if theta != 0:
    theta=90-theta
  else:
    theta = int(theta)
  while n < nLayers:
    if theta > 0:
        arr=np.loadtxt(f"{path}/csvs/{gType}_{material}_slope{theta}_{depthF}_layer{n}_{resOG}.csv", delimiter=',',dtype=np.complex128).view(complex)
    else:
        arr=np.loadtxt(f"{path}/csvs/{gType}_{material}_slope{theta}_layer{n}_{resOG}.csv", delimiter=',',dtype=np.complex128).view(complex)
    
    count=0
    while count < rowPLayer:
        profA[place+count]=upScale(arr[2,:], scaleFac)
        count=count+1

    n=n+1
    place=n*count
  #profA=(profA/10).astype(np.uint8)
  i=0
  j=0
  x,y=np.shape(profA)
  while i < x:
      j=0
      while j <y:
          if math.isclose(profA[i][j].real,1,abs_tol=0.1):
              profA[i][j]=1
          else:
              profA[i][j]=0
          j=j+1
      i=i+1
  profA=profA*255
  prof_repeat = np.zeros([profA.shape[0],3*profA.shape[1]])
  row = np.array([])
  count=0
  for i in profA:
    row = np.array([])

    row = np.append(row,i)
    row = np.append(row,i)
    row = np.append(row,i)

    

    prof_repeat[count,:] = row
    count+=1
  im = Image.fromarray(prof_repeat)
  im=im.convert('L')
#   if im.mode != 'RGB':
#     im = im.convert('RGB')
  im.save(f"{path}/profiles/sloped{theta}_depth{depthF}_res{resOG}.jpg")
  
  return im
