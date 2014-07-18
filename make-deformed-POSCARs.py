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

usage= '%prog [options] [POSCAR]'

parser= optparse.OptionParser(usage=usage)
parser.add_option("-d","--dev",dest="dev",type="float",default=0.05,
                  help="maximum value of each strain element.")
parser.add_option("-n","--num-dev",dest="ndev",type="int",default=2,
                  help="number of devision in each strain element.")
parser.add_option("--offset",dest="offset",type="int",default=0,
                  help="offset of sequential number in output file.")

(options,args)= parser.parse_args()

dev= options.dev
ndev= options.ndev
offset= options.offset

fname= args[0]
poscar= POSCAR()
poscar.read(fname=fname)

#...original a vectors
ho= copy.deepcopy(poscar.h)

h = np.zeros((3,3),dtype=float)

inc= offset

de11= 2*dev/ndev
de22e33= 2*dev/ndev
dg12= 2*dev/ndev
dg23g31= 2*dev/ndev
for ne11 in range(ndev+1):
    e11= -dev +ne11*de11
    for ne22e33 in range(ndev+1):
        e22e33= -dev +ne22e33*de22e33
        for ng12 in range(ndev+1):
            g12= -dev +ng12*dg12
            for ng23g31 in range(ndev+1):
                g23g31= -dev +ng23g31*dg23g31
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
                poscar.write(fname=fname+'-{0:03d}'.format(inc))

