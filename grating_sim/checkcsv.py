import numpy as np
import cmath
from IPython import display
from PIL import Image
import matplotlib.pyplot as plt




def Check(res,er, material, gType, path):
    duty=0.5
    arr=np.ones([res,res])
    arrIm=arr
    arr=(1.0006+0j)*arr
    i,j=0,0
    
    #permittivity
    while i <duty*res:
        while j < duty*res:
            arr[i,j]=er
            arrIm[i,j]=500
            j=j+1
        j=0
        i=i+1
    i,j=int(duty*res),int(duty*res)
    while i >=duty*res and i<res:
        while j >= duty*res and j <res:
            arr[i,j]=er
            arrIm[i,j]=500
            j=j+1
        j=int(duty*res)
        i=i+1
        
    np.savetxt(f'{path}/csvs/{gType}_{material}_slope0_layer0_{res}.csv', arr, delimiter=',')
    i,j=0,0
    arrP=np.ones([res,res])
    np.savetxt(f'{path}/csvs/U{res}.csv', arrP, delimiter=',')
    im = Image.fromarray(arrIm)
    plt.figure()
    plt.imshow(im)
    display.display(plt.gcf())
    return 1

def CheckErr(res,er, material, gType, err, path):
    duty=0.5
    err=float(err)
    arr=np.ones([res,res])
    arrIm=arr
    arr=(1.000536+0j)*arr
    e_cells=int(duty*res*0.5*err)
    i,j=e_cells,e_cells
    print(f'e_cells={e_cells}')
    #permittivity
    while i <int(duty*res-e_cells):
        while j < int(duty*res-e_cells):
            arr[i,j]=er
            arrIm[i,j]=500
            j=j+1
        j=e_cells
        i=i+1
    i,j=int(duty*res+e_cells),int(duty*res+e_cells)
    
    while i >=int(duty*res+e_cells) and i<int(res-e_cells):
        while j >=int(duty*res+e_cells) and j <int(res-e_cells):
            arr[i,j]=er
            arrIm[i,j]=500
            j=j+1
        j=int(duty*res+e_cells)
        i=i+1
        
    np.savetxt(f'{path}/csvs/{gType}_{material}_slope0_layer0_{res}.csv', arr, delimiter=',')
    arrP=np.ones([res,res])
    np.savetxt(f'{path}/csvs/U{res}.csv', arrP, delimiter=',')
    im = Image.fromarray(arrIm)
    plt.figure()
    plt.imshow(im)
    display.display(plt.gcf())
    return 1





def CheckCoat(res,er, material, gType,si, path):
    duty=0.5
    arr=np.ones([res,res])
    arr=(1.000536+0j)*arr
    i=0
    j=int(res/2)
    mi,ma=int(res/2)-1,int(res/2)+1
    switch=False
    while i < res:
        while mi<j<ma:
            arr[i,j]=er
            j=j+1
        if mi>-1 and ma<res+1 and  not switch:
            mi=mi-1
            ma=ma+1
        else:
            switch=True
            mi=mi+1
            ma=ma-1
        j=mi+1
        i=i+1 
    np.savetxt(f'{path}/csvs/{gType}_{material}_slope0_layer0_{res}.csv', arr, delimiter=',')
    i,j=0,0
    arrP=np.ones([res,res])
    np.savetxt(f'{path}/csvs/U{res}.csv', arrP, delimiter=',')
    
    arr=np.ones([res,res])
    arr=er*arr
    i=0
    j=int(res/2)
    mi,ma=int(res/2)-1,int(res/2)+1
    switch=False
    while i < res:
        while mi<j<ma:
            arr[i,j]=si
            j=j+1
        if mi>-1 and ma<res+1 and  not switch:
            mi=mi-1
            ma=ma+1
        else:
            switch=True
            mi=mi+1
            ma=ma-1
        j=mi+1
        i=i+1
    np.savetxt(f'{path}/csvs/{gType}_{material}_slope0_layer1_{res}.csv', arr, delimiter=',')
    return 2


def CheckDiag(res,er, material, gType, path):
    arr=np.ones([res,res])
    arrIm=500*arr
    arr=(1.000536+0j)*arr
    i=0
    j=int(res/2)
    mi,ma=int(res/2)-1,int(res/2)+1
    switch=False
    while i < res:
        while mi<j<ma:
            arr[i,j]=er
            arrIm[i,j]=1
            j=j+1
        if mi>-1 and ma<res+1 and  not switch:
            mi=mi-1
            ma=ma+1
        else:
            switch=True
            mi=mi+1
            ma=ma-1
        j=mi+1
        i=i+1
    np.savetxt(f'{path}/csvs/{gType}_{material}_slope0_layer0_{res}.csv', arr, delimiter=',')
    arrP=np.ones([res,res])
    np.savetxt(f'{path}/csvs/U{res}.csv', arrP, delimiter=',')
    im = Image.fromarray(arrIm)
    plt.figure()
    plt.imshow(im)
    display.display(plt.gcf())
    return 1
    
def CheckDiagErr(res,er, material, gType,err ,path):
    err=float(err)
    cells=int(err*res/2)
    inverse=input("Would you like the smaller squares extruded? Yes/No? If No they will be sunken")
    sunken = False
    if inverse.lower() == 'no':
        sunken = True
    arr=np.ones([res,res])
    if sunken:
        arrIm=arr
        arr=er*arr
    else:
        arrIm=500*arr
        arr=(1.000536+0j)*arr
    i=cells
    j=int(res/2)
    mi,ma=int(res/2)-1,int(res/2)+1
    switch=False
    while i < res-cells:
        while mi<j<ma:
            if sunken:
                arr[i,j]=1.000536+0j
                arrIm[i,j]=500
            else:
                arr[i,j]=er
                arrIm[i,j]=1
            j=j+1
        if mi>-1+cells and ma<res+1-cells and  not switch:
            mi=mi-1
            ma=ma+1
        else:
            switch=True
            mi=mi+1
            ma=ma-1
        j=mi+1
        i=i+1
    np.savetxt(f'{path}/csvs/{gType}_{material}_slope0_layer0_{res}.csv', arr, delimiter=',')
    arrP=np.ones([res,res])
    np.savetxt(f'{path}/csvs/U{res}.csv', arrP, delimiter=',')
    im = Image.fromarray(arrIm)
    plt.figure()
    plt.imshow(im)
    display.display(plt.gcf())
    return 1