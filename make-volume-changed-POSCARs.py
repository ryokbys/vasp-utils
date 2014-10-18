#!/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------
# Make volume-changed POSCAR files from the non-deformed POSCAR file.
# Deformation is performed by changing the lattice constant..
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

#.....original lattice constant
afac0= copy.deepcopy(poscar.afac)

inc= offset

da= 2 *afac0*dev/ndev
al0= afac0 *(1.0-dev)
for na in range(ndev+1):
    poscar.afac= al0 +da*na
    inc += 1
    poscar.write(fname=fname+'-{0:03d}'.format(inc))
