import numpy as np
import cmath
import math
from IPython import display
from PIL import Image
import matplotlib.pyplot as plt
path = 'grating_sim'

def Square(res,er, material, gType, path):
    duty=float(input("What duty factor would you like for the squares? Eg. 0.3 for squares which have a width of 0.3*period."))
    arr=np.ones([res,res])
    arrIm=500*arr
    arr=(1.000536+0j)*arr
    i,j=int((1-duty)/2*res),int((1-duty)/2*res)
    
    #permittivity
    while i>=(1-duty)/2*res and  i<(1-(1-duty)/2)*res:
        while j>=(1-duty)/2*res and  j<(1-(1-duty)/2)*res:
            arr[i,j]=er
            arrIm[i,j]=1
            j=j+1
        j=int((1-duty)/2*res)
        i=i+1

  
    np.savetxt(f'{path}/csvs/{gType}_{material}_slope0_layer0_{res}.csv', arr, delimiter=',')
    arrP=np.ones([res,res])
    np.savetxt(f'{path}/U{res}.csv', arrP, delimiter=',')
    im = Image.fromarray(arrIm)
    plt.figure()
    plt.imshow(im)
    display.display(plt.gcf())
    return 1


def Circ(res,er,material,gType, path):
    scale=input("What size would you like the circles? Enter a scale factor, eg. 0.8 for circle diameter 80% of unit cell")
    print(res)
    print(er)
    inverse=input("Would you like the circles extruded? Yes/No? If No they will be sunken")
    sunken = False
    if inverse.lower() == 'no':
        sunken = True
    r=int(float(scale)*res/2)
    print(r)
    arr=np.ones([res,res])
    
    if sunken:
        print("The circles will be sunken\n")
        arrIm=arr
        arr=er*arr
        
    else:
        arrIm=500*arr
        arr=(1.000536+0j)*arr
    i,j=0,0
    temp=0
    while i < res:
        while j<res:
            eqn=(-1*i+res/2)**2+(j-res/2)**2

            if math.isclose(eqn,r**2,rel_tol=0.005):
                temp=j
                while j < res-temp:
                    if sunken:
                        arr[i,j]=1.000536+0j
                        arrIm[i,j]=500
                    else:
                        arr[i,j]=er
                        arrIm[i,j]=1
                    j=j+1
            j=j+1
        i=i+1
        j=0
    np.savetxt(f'{path}/csvs/{gType}_{material}_slope0_layer0_{res}.csv', arr, delimiter=',')
    arrP=np.ones([res,res])
    np.savetxt(f'{path}/csvs/U{res}.csv', arrP, delimiter=',')
    im = Image.fromarray(arrIm)
    plt.figure()
    plt.imshow(im)
    display.display(plt.gcf())
    return 1          