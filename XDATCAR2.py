#!/bin/env python
# -*- coding: utf-8 -*-
"""
The python script XDATCAR2.py converts POSCAR and XDATCAR file to
sequential files specified by the user.
This script can be only applicable to VASP 5.3, but not to 4.6,
because of the XDATCAR file-format.

USAGE:
    $ ./XDATCAR2.py

INPUT: (these files must be in the working directory)
    - INCAR (to get ISIF and POTIM value)
    - POSCAR (for the cell information)
    - XDATCAR (atom configuration per each step)
"""

import os
import optparse
from AtomSystem import AtomSystem
import numpy as np

def output_AtomSystem(aSys,format,num):
    if out_format[0] in ('a','A'):
        aSys.write_akr('akr{0:04d}'.format(num))
    elif out_format[0] in ('p','P'):
        aSys.write_POSCAR('POSCAR{0:04d}'.format(num))
    return

def parse_INCAR(fname='INCAR'):
    """
    Parse INCAR file and returns a dictionary variable.
    """
    fincar= open(fname,'r')
    incar= {}
    for line in fincar.readlines():
        if line[0]=='#': # skip lines starting with #
           continue
        data=line.replace('=',' ').split()
        if len(data)<2:
            continue
        incar[data[0]]= data[1]
    fincar.close()
    return incar

#================================================== main routine
if __name__ == '__main__':
    usage= '%prog [options]'

    parser= optparse.OptionParser(usage=usage)
    parser.add_option("-s",dest="format",type="string",default="POSCAR",
                      help="output file format. Default is POSCAR.")
    (options,args)= parser.parse_args()

    out_format= options.format
    #...check output format
    if not out_format[0] in ('a','A','p','P'):
        print ' ERROR: Output format must be akr or POSCAR.'
        exit()

    #...check INCAR file and parse it
    if not os.path.exists('./INCAR'):
        print ' ERROR: INCAR does not exist here.'
        exit()
    incar= parse_INCAR('INCAR')
    # if int(incar['ISIF']) > 2:
    #     print ' ERROR: ISIF>2 in INCAR'
    #     print '   This script would not be applicable'\
    #         +' to this XDATCAR format.'
    #     exit()
    nstep= int(incar['NSW'])
    if 'NBLOCK' in incar:
        nblock=int(incar['NBLOCK'])
    else:
        nblock= 1
    nstep= nstep/nblock
    dt= float(incar['POTIM'])*nblock # dt in ft
    
    print "out_format =",out_format
    print "nstep      =",nstep
    print "dt         =",dt

    #...read POSCAR as 0th step
    if not os.path.exists('./POSCAR'):
        print ' ERROR: POSCAR does not exist here.'
        exit()
    aSys= AtomSystem()
    aSys.read_POSCAR('./POSCAR')

    #...output 0th step
    output_AtomSystem(aSys,out_format,0)

    #...read XDATCAR after 0th step
    if not os.path.exists('./XDATCAR'):
        print ' ERROR: XDATCAR does not exist here.'
        exit()
    f= open('XDATCAR','r')
    line1= f.readline()
    alc= float(f.readline().split()[0])
    a1= [ float(x) for x in f.readline().split()]
    a2= [ float(x) for x in f.readline().split()]
    a3= [ float(x) for x in f.readline().split()]
    line6= f.readline() # Species names
    nas= [ int(n) for n in f.readline().split() ] # Num of atoms
    #....count total num of atoms
    natm= 0
    for i in nas:
        natm += i
    print 'number of atoms = ',natm
    ra = np.zeros((natm,3),dtype=float)
    rap= np.zeros((natm,3),dtype=float)
    va = np.zeros((natm,3),dtype=float)
    vi = np.zeros(3,dtype=float)
    for istp in range(nstep):
        if int(incar['ISIF']) > 2 and not istp==0:
            line1= f.readline()
            alc= float(f.readline().split()[0])
            a1= [ float(x) for x in f.readline().split()]
            a2= [ float(x) for x in f.readline().split()]
            a3= [ float(x) for x in f.readline().split()]
            line6= f.readline() # Species names
            line7= f.readline() # num of atoms
            # print ' line6=',line6
            # print ' line7=',line7
        line= f.readline()
        n= 0
        rap[:,:]= ra[:,:]
        for ia in range(natm):
            line= f.readline()
            if not line:
                exit()
            buff= line.split()
            ra[ia,0]= float(buff[0])
            ra[ia,1]= float(buff[1])
            ra[ia,2]= float(buff[2])
            va[ia,0:3]= (ra[ia,0:3] -rap[ia,0:3])
            va[ia,0]= (va[ia,0]-round(va[ia,0]))/dt
            va[ia,1]= (va[ia,1]-round(va[ia,1]))/dt
            va[ia,2]= (va[ia,2]-round(va[ia,2]))/dt
            if istp == 0:
                va[ia,:]= 0.0
            #.....scale velocity to [A/fs]
            vi[0]= (va[ia,0]*a1[0] +va[ia,1]*a2[0] +va[ia,2]*a3[0])*alc
            vi[1]= (va[ia,0]*a1[1] +va[ia,1]*a2[1] +va[ia,2]*a3[1])*alc
            vi[2]= (va[ia,0]*a1[2] +va[ia,1]*a2[2] +va[ia,2]*a3[2])*alc
            aSys.atoms[n].set_pos(ra[ia,0],ra[ia,1],ra[ia,2])
            aSys.atoms[n].set_vel(vi[0],vi[1],vi[2])
            n+=1
        output_AtomSystem(aSys,out_format,istp+1)
