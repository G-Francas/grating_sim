
import numpy as np
def Slopecsv(res,theta,depthF, material, gType, er, path): #depth is fraction of wavelength
  nm= 10**(-9)
  um=10**(-6)
  duty=0.5
  

  
  #values for air
  e=1.0006
  u= 1
  mat_u=1
  arr=np.ones([res,res])
  Uarr=arr
  np.savetxt(f'{path}/csvs/U{res}.csv', Uarr, delimiter=',')

  arr=(1+0j)*arr
  if theta > 0:
      thetaR=np.deg2rad(theta)
      nLayer=int(np.divide(2,3)*res*depthF*np.tan(thetaR))
      arrE=er*arr
      count=0
      i=0
      j=int(res/4)
      print(f'creating {nLayer} csv files for simulation...\n')
      while count <= nLayer:
        arrE=er*arr
        i=0
        j=int(res/4+count)
        #permittivity
        while i <res:
            while j >= res/4+count and j < 3*res/4-count: 
                arrE[i,j]=e
                j=j+1
            j=int(res/4+count)
            i=i+1   
        np.savetxt(f'{path}/csvs/{gType}_{material}_slope{90-theta}_{depthF}_layer{count}_{res}.csv', arrE, delimiter=',')
        count=count+1
  elif theta ==0:
    count=0
    nLayer=1
    i,j=0,int(res/4)
    arrE=er*arr
    arrU=mat_u*arr
    while i < res:
        
        while j>=int(res/4) and j < int(3*res/4):
            arrE[i,j]=e
            arrU[i,j]=u
            j=j+1
        j=int(res/4)
        i=i+1
    print(path)
    np.savetxt(f'{path}/csvs/{gType}_{material}_slope0_layer0_{res}.csv', arrE, delimiter=',')
    np.savetxt(f'{path}/csvs/U{res}.csv', Uarr, delimiter=',')
  else:
    print('Theta must be >=0')
  return nLayer



