import numpy as np
def SlopeNew(res,theta,depthF, period, wavelength, material, gType, er, path): #depth is fraction of wavelength
  nm= 10**(-9)
  um=10**(-6)
  duty=0.5
  
  periodF = period/wavelength
  dres = depthF/periodF*res
  nLayers = int(input("How many layers should be used for the simulation? (<100): "))
  dx = np.tan(np.deg2rad(90-theta))/nLayers*dres


  ##refractive index vals at 400nm
  Air_n = 1.000536
  Si_n = 5.623
  Al_n = 0.375150842
  Ag_n = 0.04572895
 



  #extinction coefficient vals at 400nm
  Air_k = 1.00000037
  Si_k = 0.326
  Al_k= 4.226433266
  Ag_k = 2.122943979

  if material == 'Silicon':
    mat_e=np.square(Si_n)
    print('grating material = silicon')
  elif material == 'Aluminium':
    mat_e=np.square(Al_n)
    print('grating material = aluminium')

  elif material == 'Silver':
    mat_e=np.square(Ag_n)
    print('grating material = silver')
  mat_u=1
  e=1.0006
  u= 1

  arr=np.ones([res,res])
  Uarr=arr
  arr=(1+0j)*arr
  print(theta)
  if theta > 0:
      print(f"new sloped")
      
      arrE=er*arr
      arrU=mat_u*arr
      count=0
      i=0
      j=int(res/4)
      print(f'creating {nLayers} csv files for simulation...\n')
      while count < nLayers:
        arrE=er*arr
        arrU=mat_u*arr
        i=0
        j=int(res/4+count*dx)
        #permittivity
        while i <res:
            while j >= res/4+count*dx and j < 3*res/4-count*dx: 
                arrE[i,j]=e
                arrU[i,j]=u
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

