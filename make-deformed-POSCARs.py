#!/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------
# Make deformed POSCAR files from the non-deformed POSCAR file.
# Deformation is performed by multiplying deformation matrix to h-mat.
#-----------------------------------------------------------------------
#

import numpy as np
import copy,optparse

from POSCAR import POSCAR

#======================================== subroutines and functions

def deform_cubic(poscar):
    """
    Deformation of the simulation cell that has cubic symmetry.
    Only uniaxial deformation for C11 and C12,
    off diagonal deformation for C44 are considered.
    Be sure that you are applying this routine to the cubic cell.
    """
    ho= copy.deepcopy(poscar.h)
    h = np.zeros((3,3),dtype=float)
    inc= _offset
    #...uniaxial deformation in x-direction (no y or z is needed)
    de11= 2*_dev/_ndev
    #print " de11 =",de11
    for ne11 in range(_ndev+1):
        e11= -_dev +ne11*de11
        #print "  e11 =",e11
        h[0,0]= ho[0,0]*(1.0+e11)
        h[0,1]= ho[0,1]
        h[0,2]= ho[0,2]
        h[1,0]= ho[1,0]
        h[1,1]= ho[1,1]
        h[1,2]= ho[1,2]
        h[2,0]= ho[2,0]
        h[2,1]= ho[2,1]
        h[2,2]= ho[2,2]
        poscar.h= h
        inc += 1
        poscar.write(fname=_fname+'-{0:03d}'.format(inc))

    #...off diagonal deformation
    dg12= 2*_dev/_ndev
    #print " dg12 =",dg12
    for ng12 in range(_ndev+1):
        g12= -_dev +ng12*dg12
        #print "  g12 =",g12
        h[0,0]= ho[0,0]
        h[0,1]= g12
        h[0,2]= g12
        h[1,0]= g12
        h[1,1]= ho[1,1]
        h[1,2]= g12
        h[2,0]= g12
        h[2,1]= g12
        h[2,2]= ho[2,2]
        poscar.h= h
        inc += 1
        poscar.write(fname=_fname+'-{0:03d}'.format(inc))
    #...restore poscar.h
    poscar.h= ho


def deform_random(poscar):
    """
    Random deformation of the simulation cell.
    """
    #...original a vectors
    ho= copy.deepcopy(poscar.h)
    h = np.zeros((3,3),dtype=float)
    
    inc= _offset
    
    de11= 2*_dev/_ndev
    de22e33= 2*_dev/_ndev
    dg12= 2*_dev/_ndev
    dg23g31= 2*_dev/_ndev
    for ne11 in range(_ndev+1):
        e11= -_dev +ne11*de11
        for ne22e33 in range(_ndev+1):
            e22e33= -_dev +ne22e33*de22e33
            for ng12 in range(_ndev+1):
                g12= -_dev +ng12*dg12
                for ng23g31 in range(_ndev+1):
                    g23g31= -_dev +ng23g31*dg23g31
                    h[0,0]= (1.0+e11)*ho[0,0] +g12         *ho[0,1] +g23g31      *ho[0,2]
                    h[0,1]= g12      *ho[0,0] +(1.0+e22e33)*ho[0,1] +g23g31      *ho[0,2]
                    h[0,2]= g23g31   *ho[0,0] +g23g31      *ho[0,1] +(1.0+e22e33)*ho[0,2]
                    h[1,0]= (1.0+e11)*ho[1,0] +g12         *ho[1,1] +g23g31      *ho[1,2]
                    h[1,1]= g12      *ho[1,0] +(1.0+e22e33)*ho[1,1] +g23g31      *ho[1,2]
                    h[1,2]= g23g31   *ho[1,0] +g23g31      *ho[1,1] +(1.0+e22e33)*ho[1,2]
                    h[2,0]= (1.0+e11)*ho[2,0] +g12         *ho[2,1] +g23g31      *ho[2,2]
                    h[2,1]= g12      *ho[2,0] +(1.0+e22e33)*ho[2,1] +g23g31      *ho[2,2]
                    h[2,2]= g23g31   *ho[2,0] +g23g31      *ho[2,1] +(1.0+e22e33)*ho[2,2]
                    poscar.h= h
                    inc += 1
                    poscar.write(fname=_fname+'-{0:03d}'.format(inc))
    #...restore poscar.h
    poscar.h= ho


#======================================== main routine hereafter

_usage= '%prog [options] [POSCAR]'
parser= optparse.OptionParser(usage=_usage)
parser.add_option("-d","--dev",dest="dev",type="float",default=0.05,
                  help="maximum value of each strain element.")
parser.add_option("-n","--num-dev",dest="ndev",type="int",default=2,
                  help="number of devision in each strain element.")
parser.add_option("-o","--offset",dest="offset",type="int",default=0,
                  help="offset of sequential number in output file."
                  +" Default value is 0.")
parser.add_option("-m","--mode",dest="mode",
                  type="string",default="random",
                  help="deformation mode setting."
                  +" random: random deformation of the cell,"
                  +" cubic: for the case of cubic symmetry.")

(options,args)= parser.parse_args()

_dev= options.dev
_ndev= options.ndev
_offset= options.offset
_mode= options.mode

_fname= args[0]
poscar= POSCAR()
poscar.read(fname=_fname)

if _mode in ("random","Random","RANDOM"):
    deform_random(poscar)
elif _mode in ("cubic","Cubic","CUBIC"):
    deform_cubic(poscar)

