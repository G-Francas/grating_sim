
import numpy as np
def Slopecsv(res,theta,depthF, material, gType, er, path): #depth is fraction of wavelength
  nm= 10**(-9)
  um=10**(-6)
  duty=0.5
  

  ##refractive index vals at 400nm
  Air_n = 1.000536
  Si_n = 5.623
  Al_n = 0.48787
  #Al_n = 0.375150842
  Ag_n = 0.04572895
 



  #extinction coefficient vals at 400nm
  Air_k = 1.00000037
  Si_k = 0.326
  Al_k = 4.8355
  #Al_k= 4.226433266
  Ag_k = 2.122943979
  print(f"Grating Material {material}, test test")

  er_si=(Si_n)**2-(Si_k)**2+2*Si_n*Si_k*1j
  if material == 'Silicon':
      er=er_si
  elif material == 'Aluminium':
      er=(Al_n)**2-(Al_k)**2+2*Al_n*Al_k*1j
  elif material == 'Silver':
      er=(Ag_n)**2-(Ag_k)**2+2*Ag_n*Ag_k*1j
  elif material == 'Gold':
      er=(Au_n)**2-(Au_k)**2+2*Au_n*Au_k*1j
  elif material == 'Titanium':
      er=(Ti_n)**2-(Ti_k)**2+2*Ti_n*Ti_k*1j
  mat_u=1
  
  #values for air
  e=1.0006
  u= 1

  arr=np.ones([res,res])
  Uarr=arr
  arr=(1+0j)*arr
  print(theta)
  if theta > 0:
      thetaR=np.deg2rad(theta)
      nLayer=int(np.divide(2,3)*res*depthF*np.tan(thetaR))
      arrE=er*arr
      arrU=mat_u*arr
      count=0
      i=0
      j=int(res/4)
      print(f'creating {nLayer} csv files for simulation...\n')
      while count <= nLayer:
        arrE=er*arr
        arrU=mat_u*arr
        i=0
        j=int(res/4+count)
        #permittivity
        while i <res:
            while j >= res/4+count and j < 3*res/4-count: 
                arrE[i,j]=e
                arrU[i,j]=u
                j=j+1
            j=int(res/4+count)
            i=i+1
            
            
        np.savetxt(f'{path}/csvs/{gType}_{material}_slope{90-theta}_{depthF}_layer{count}_{res}.csv', arrE, delimiter=',')
        np.savetxt(f'{path}/csvs/U{res}.csv', Uarr, delimiter=',')
    
        
    
        count=count+1
  elif theta ==0:
    count=0
    nLayer=1
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
  return nLayer



