import numpy as np
import cmath
import math
from py_pol import *
from py_pol.stokes import Stokes, create_Stokes, degrees
from py_pol.jones_vector import Jones_vector, create_Jones_vectors


def getAngles(har,wavelength,period):
    modes=np.linspace(-int(har/2),int(har/2), num=har)
    angles=np.arcsin(modes*wavelength/period)
    return angles
    
    
def transform(RX,RY,RZ,wavelength,period,axis,clock):
    angle = np.arcsin(wavelength/period)
    vec=np.array([complex(RX[2,1]), complex(RY[2,1]), complex(RZ[2,1])], dtype='complex')
    print(f"before transform {vec}\n")
    if axis is 'x':
        if clock:
            angle=2*np.pi-angle
        mat=np.array([1, 0, 0, 0, np.cos(angle), -1*np.sin(angle), 0,np.sin(angle),np.cos(angle)])
        mat=mat.reshape(3,3)
        jones=np.dot(mat,vec)
        print(f"the Jones vector: {jones}\n")
        Ex=complex(str(jones[0]))
        Ey=complex(str(jones[1]))
        j0=Jones_vector('jones')
        j0.from_components(np.array([Ex]),np.array([Ey]))
        s0=Stokes('stoked')
        s0.from_Jones(j0)
        check=s0.checks.is_physical()
        print(f"Is the result physically viable?: {check}\n")
    return s0
    
