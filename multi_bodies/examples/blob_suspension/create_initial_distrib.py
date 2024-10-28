import argparse
import numpy as np
import scipy.optimize as scop
import subprocess
from functools import partial
import sys
import os
import time
import math as m
# Try to import numba
try:
  from numba import njit, prange
except ImportError:
  print('numba not found')

if __name__ ==  '__main__':

  # Particle radius
  a = 1

  # Number of particle along each direction
  Nx = 10
  Ny = 10
  Nz = 10

  Np = Nx*Ny*Nz

  # Domain boundaries
  xmin = 0
  xmax = 20*a
  ymin = xmin
  ymax = xmax
  zmin = 1.1*a
  zmax = 20*a

  # Generate particle positions
  x = np.linspace(xmin,xmax,Nx)
  y = np.linspace(ymin,ymax,Ny)
  z = np.linspace(zmin,zmax,Nz)
  
  xx, yy, zz = np.meshgrid(x,y,z, indexing='ij')
  # add some randomness
  fac = 0/2
  xx += fac*(np.random.rand(Nx,Ny,Nz)-0.5) 
  yy += fac*(np.random.rand(Nx,Ny,Nz)-0.5) 
  zz += fac*(np.random.rand(Nx,Ny,Nz)-0.5) 
    
  xxv = np.reshape(xx,(Np,1))
  yyv = np.reshape(yy,(Np,1))
  zzv = np.reshape(zz,(Np,1))
  # Initial position
  pos = np.concatenate((xxv, yyv, zzv),axis=1)
  # Initial orientation
  quat = np.concatenate((np.zeros((Np,1)), np.ones((Np,1)), np.zeros((Np,1)), np.zeros((Np,1))),axis=1)

  to_save =  np.concatenate((pos,quat),axis=1)
  
  fname = 'sphere_array.clones'
  np.savetxt(fname, to_save, header = str(Np), comments='')
