import numpy as np
def SlopeNew(res,theta,depthF, period, wavelength, material, numLayer,gType, er, path): #depth is fraction of wavelength
  nm= 10**(-9)
  um=10**(-6)
  duty=0.5
  
  periodF = period/wavelength
  dres = depthF/periodF*res
  nLayers = int(numLayer)
  dx = np.tan(np.deg2rad(theta))/nLayers*dres
  
  print(f"PeriodF = {periodF}, dres = {dres}, dx = {dx}")


 
  mat_u=1
  e=1.0006
  u= 1

  arr=np.ones([res,res])
  Uarr=arr
  arr=(1+0j)*arr
  print(theta)
  if theta > 0:
      count=0
      print(f'creating {nLayers} csv files for simulation...\n')
      while count < nLayers:
        arrE=er*arr
        arrU=mat_u*arr
        i=0
        j=int(res/4+count*dx)
        #permittivity
        while i <res:
            while j >= int(res/4+count*dx) and j < int(3*res/4-count*dx): 
                arrE[i,j]=e
                j=j+1
            j=int(res/4+count*dx)
            i=i+1
            
            
        np.savetxt(f'{path}/csvs/{gType}_{material}_slope{90-theta}_{depthF}_layer{count}_{res}.csv', arrE, delimiter=',')
        np.savetxt(f'{path}/csvs/U{res}.csv', Uarr, delimiter=',')
    
        
    
        count=count+1
  elif theta ==0:
    count=0
    nLayers=1
    i,j=0,int(res/4)
    arrE=er*arr
    arrU=mat_u*arr
    while i < res:
        
        while j>=int(res/4) and j < int(3*res/4):
            arrE[j,i]=e
            arrU[j,i]=u
            j=j+1
        j=int(res/4)
        i=i+1
    print(path)
    np.savetxt(f'{path}/csvs/{gType}_{material}_slope0_layer0_{res}.csv', arrE, delimiter=',')
    np.savetxt(f'{path}/csvs/U{res}.csv', Uarr, delimiter=',')
  else:
    print('Theta must be >=0')
  return nLayers

