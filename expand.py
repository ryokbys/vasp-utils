#!/bin/env python
# -*- coding: utf-8 -*-
"""
Expand atomic system from a POSCAR file by copying the system
along a1,a2,a3 direction (n1,n2,n3).


USAGE:
    $ python ./expand-POSCAR.py [options] POSCAR n1 n2 n3

INPUT: (these files must be in the working directory)
    - POSCAR (for the cell information)
"""

import os
import optparse
from atom_system import AtomSystem

aSys= AtomSystem()

#================================================== main routine
if __name__ == '__main__':
    usage= '$ python %prog [options] ./POSCAR n1 n2 n3'

    parser= optparse.OptionParser(usage=usage)
    parser.add_option("-o",dest="outfname",type="string", \
                      default="POSCAR.expand", \
                      help="output file name. Default is POSCAR.expand.")
    (options,args)= parser.parse_args()

    outfname= options.outfname

    #...read POSCAR as 0th step
    if not len(args)==4:
        print '[Error] Num of arguments wrong!!!'
        print usage
        exit()
    infname= args[0]
    n1= int(args[1])
    n2= int(args[2])
    n3= int(args[3])
    if not os.path.exists(infname):
        print '[Error] File does not exist !!!'
        exit()
    aSys.read_POSCAR(infname)

    aSys.expand(n1,n2,n3)
    aSys.write_POSCAR('POSCAR.expand')
    print 'POSCAR.expand was written. Please check it.'
    
