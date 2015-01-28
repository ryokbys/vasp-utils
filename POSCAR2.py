#!/bin/env python
# -*- coding: utf-8 -*-
"""
The python script POSCAR2.py converts POSCAR file to
sequential files specified by the user.
This script can be only applicable to VASP 5.3, but not to 4.6,
because of the XDATCAR file-format.

USAGE:
    $ python ./POSCAR2.py [options] POSCAR

INPUT: (these files must be in the working directory)
    - POSCAR (for the cell information)
"""

import os
import optparse
from AtomSystem import AtomSystem


#================================================== main routine
if __name__ == '__main__':
    usage= 'python %prog [options] ./POSCAR'

    parser= optparse.OptionParser(usage=usage)
    parser.add_option("-s",dest="format",type="string",default="akr",
                      help="output file format. Default is POSCAR.")
    parser.add_option("-o",dest="outfname",type="string",default="akr0000",
                      help="output file name. Default is akr0000.")
    (options,args)= parser.parse_args()

    out_format= options.format
    outfname= options.outfname
    #...check output format
    if not out_format[0] in ('a','p'):
        print ' ERROR: Output format must be akr or pmd.'
        exit()

    #...read POSCAR as 0th step
    if len(args)==0 and not os.path.exists('./POSCAR'):
        print ' ERROR: Any POSCAR file have not been specified.'
        exit()
    elif len(args)==0:
        infname= './POSCAR'
    else:
        infname= args[0]
    aSys= AtomSystem()
    aSys.read_POSCAR(infname)

    if out_format[0] in ('a'):
        aSys.write_akr(outfname)
    elif out_format[0] in ('p'):
        aSys.write_pmd(outfname)

