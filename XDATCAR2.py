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
    - INCAR (to get ISIF value)
    - POSCAR (for the cell information)
    - XDATCAR (atom configuration per each step)
"""

import os
import optparse
from AtomSystem import AtomSystem

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
    if int(incar['ISIF']) > 2:
        print ' ERROR: ISIF>2 in INCAR'
        print '   This script would not be applicable'\
            +' to this XDATCAR format.'
        exit()
    nstep= int(incar['NSW'])
    if 'NBLOCK' in incar:
        nblock=int(incar['NBLOCK'])
    else:
        nblock= 1
    nstep= nstep/nblock

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
    for istp in range(nstep):
        line= f.readline()
        n= 0
        for ns in range(len(nas)):
            for ia in range(nas[ns]):
                line= f.readline()
                if not line:
                    exit()
                xi= [ float(x) for x in line.split()]
                aSys.atoms[n].set_pos(xi[0],xi[1],xi[2])
                n+=1
        output_AtomSystem(aSys,out_format,istp+1)
