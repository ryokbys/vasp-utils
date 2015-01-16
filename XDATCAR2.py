#!/bin/env python
# -*- coding: utf-8 -*-
"""
The python script XDATCAR2.py converts POSCAR and XDATCAR file to
sequential files specified by the user.
This script can be only applicable to VASP 5.3, but not to 4.6,
because of the format of XDATCAR.

USAGE:
    $ ./XDATCAR2.py

INPUT: (these files must be in the working directory)
    - POSCAR (for the cell information)
    - XDATCAR (atom configuration per each step)
"""

import os
from AtomSystem import AtomSystem

def output_AtomSystem(aSys,format,num):
    if out_format[0] in ('a','A'):
        aSys.write_akr('akr{0:04d}'.format(num))
    else if out_format[0] in ('p','P'):
        aSys.write_POSCAR('POSCAR{0:04d}'.format(num))
    return

#================================================== main routine
if __name__ == '__main__':
    usage= '%prog [options]'

    parser= optparse.OptionParser(usage=usage)
    parser.add_option("-s",dest="format",type="string",default="akr",
                      help="output file format.")

    (options,args)= parser.parse_args()

    out_format= options.format
    #...check output format
    if not out_format[0] in ('a','A','p','P'):
        print ' ERROR: Output format must be akr or POSCAR.'
        exit()

    #...read POSCAR as 0th step
    if not os.path.exists('./POSCAR'):
        print ' ERROR: POSCAR does not exist here.'
        exit()
    aSys= AtomSystem.read_POSCAR('./POSCAR')

    #...output 0th step
    output_AtomSystem(aSys,out_format,0)

    #...read XDATCAR after 0th step
    if not os.path.exists('./XDATCAR'):
        print ' ERROR: XDATCAR does not exist here.'
        exit()
    f= open('XDATCAR','r')
    natm= int(f.readline.split().[0])
    
