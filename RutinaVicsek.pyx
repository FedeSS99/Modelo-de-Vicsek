# cython: language_level = 3

import cython
import numpy as np
cimport numpy as np

ctypedef np.float64_t Dtype_t

cdef extern from "math.h":
    Dtype_t sin(Dtype_t arg) 
    Dtype_t cos(Dtype_t arg)  
    Dtype_t atan2(Dtype_t argy, Dtype_t argx) 

from libc.stdlib cimport rand
cdef extern from 'limits.h':
    Dtype_t RAND_MAX


@cython.wraparound(False)
@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.cdivision(True)
def ActualizarFlocking(Dtype_t Ruido, Dtype_t dt, Dtype_t v0, Dtype_t lx, Dtype_t ly, Dtype_t r, np.ndarray[Dtype_t, ndim=2] Pos,np.ndarray[Dtype_t, ndim=2] Velocidad,np.ndarray[Dtype_t, ndim=2] Theta, np.ndarray[Dtype_t, ndim=2] ThetaCopia):
    cdef int N_particulas = <int>Pos.shape[0]
    cdef int n,m
    cdef Dtype_t sum_cos, sum_sen, ParticulaCercana
    cdef Dtype_t PromedioCos, PromedioSen

    for n in range(N_particulas):
        sum_cos = 0.0
        sum_sen = 0.0

        Pos[n,0] += Velocidad[n,0]*dt
        Pos[n,1] += Velocidad[n,1]*dt

        if Pos[n,0] < 0.0:
            Pos[n,0] = <Dtype_t>lx + Pos[n,0]
        elif Pos[n,0] > lx:
            Pos[n,0] = <Dtype_t>lx - Pos[n,0]

        if Pos[n,1] < 0.0:
            Pos[n,1] = <Dtype_t>ly + Pos[n,1]
        elif Pos[n,1] > ly:
            Pos[n,1] = <Dtype_t>ly - Pos[n,1]

        for m in range(N_particulas):
            if n == m:
                continue
            else:
                ParticulaCercana = (Pos[m,0]-Pos[n,0])**2.0 + (Pos[m,1]-Pos[n,1])**2.0
                if ParticulaCercana < r*r:
                    sum_cos = sum_cos + cos( ThetaCopia[m,0] )
                    sum_sen = sum_sen + sin( ThetaCopia[m,0] )
        
        PromedioCos = <Dtype_t>sum_cos/<Dtype_t>(N_particulas-1)
        PromedioSen = <Dtype_t>sum_sen/<Dtype_t>(N_particulas-1)

        Theta[n,0] = atan2(PromedioSen, PromedioCos)
        
        Theta[n,0] = Theta[n,0] + Ruido*(<Dtype_t>rand()/RAND_MAX-0.5)

        Velocidad[n,0] = v0*cos(Theta[n,0])
        Velocidad[n,1] = v0*sin(Theta[n,0])
