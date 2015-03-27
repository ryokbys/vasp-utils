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

aSys= AtomSystem()

def change_species(sid1,sid2,sid3):
    global aSys
    for ia in range(aSys.num_atoms()):
        if aSys.atoms[ia].sid == 1:
            aSys.atoms[ia].set_sid(sid1)
        elif aSys.atoms[ia].sid == 2:
            aSys.atoms[ia].set_sid(sid2)
        elif aSys.atoms[ia].sid == 3:
            aSys.atoms[ia].set_sid(sid3)

#================================================== main routine
if __name__ == '__main__':
    usage= 'python %prog [options] ./POSCAR'

    parser= optparse.OptionParser(usage=usage)
    parser.add_option("-s",dest="format",type="string",default="akr",
                      help="output file format. Default is POSCAR.")
    parser.add_option("-o",dest="outfname",type="string",default="akr0000",
                      help="output file name. Default is akr0000.")
    parser.add_option("--sid1",dest="sid1",type="int",default=1,
                      help="species-ID for pmd/smd of VASP species-ID 1.")
    parser.add_option("--sid2",dest="sid2",type="int",default=2,
                      help="species-ID for pmd/smd of VASP species-ID 2.")
    parser.add_option("--sid3",dest="sid3",type="int",default=3,
                      help="species-ID for pmd/smd of VASP species-ID 3.")
    (options,args)= parser.parse_args()

    out_format= options.format
    outfname= options.outfname
    sid1= options.sid1
    sid2= options.sid2
    sid3= options.sid3
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
    #aSys= AtomSystem()
    aSys.read_POSCAR(infname)

    change_species(sid1,sid2,sid3)

    if out_format[0] in ('a'):
        aSys.write_akr(outfname)
    elif out_format[0] in ('p'):
        aSys.write_pmd(outfname)

