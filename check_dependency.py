#!/usr/bin/env python
"""
Check dependency of energy on ENCUT, KPOINTS, and size of the system.

Usage:
  check_dependency.py prepare [options]
  check_dependency.py gather

Options:
  -h, --help   Show this help message and exit.
  --kmin=KMIN  Minimum length of k-point division. [default: 1]
  --kmax=KMAX  Maximum length of k-point division. [default: 20]
  --knum=KNUM  Number of divisions between KMIN and KMAX. [default: 1]
  --emin=EMIN  Minimum energy cutoff. [default: 100]
  --emax=EMAX  Maximum energy cutoff. [default: 700]
  --enum=ENUM  Number of divisions between EMIN and EMAX. [default: 1]
  --ldiv=LDIV  LDIV is multiplied to lattice constant to get max and min of the system size.
               [default: 0.1]
  --lnum=LNUM  Number of divisions bewteen l*(1.0-LDIV) and l*(1.0+LDIV).
               [default: 1]
"""

__author__ = "Ryo KOBAYASHI"
__version__ = "0.1a"

import os,sys,re,glob
from docopt import docopt

from pymatgen.io.vaspio.vasp_output import Vasprun

_dname_prefix= "calc-"

_end_msg_prepare="""Preparation done.
Perform vasp in each directory, like,
  $ for dir in calc-0????; do cp run_vasp.sh $dir/; done
  $ for dir in calc-0????; do cd $dir; qsub run_vasp.sh; cd ..; done
And then, perform check_dependency.py again with gather subcommand as
  $ python check_dependency gather """

_out_file="out.gather"
_end_msg_gather="""Gathered information is written in {0}. """.format(_out_file)

def check_vasp_ready():
    for file in ('INCAR','KPOINTS','POSCAR','POTCAR'):
        if not os.path.exists(file):
            print("Error: file {0} does not exist here !!!".format(file))
            print("  At least, you need INCAR, POSCAR, POSCAR, and POTCAR files.")
            sys.exit()
    return True

def prepare_for_vasp(kmin,kmax,knum,emin,emax,enum,ldiv,lnum):
    check_vasp_ready()
    ncalc= 0
    de= (emax-emin)/(enum-1)
    dl= 2*ldiv/(lnum-1)
    lmin= 1.0 -ldiv
    for ie in range(enum):
        encut= emin + de*ie
        for il in range(lnum):
            lnow= lmin +dl*il
            ncalc += 1
            dname= _dname_prefix+"{0:05d}".format(ncalc)
            os.system("mkdir -p "+dname)
            os.system("cp INCAR KPOINTS POSCAR POTCAR {0}/".format(dname))
            replace_ENCUT(dname+'/INCAR',encut)
            replace_lattice_constant(dname+'/POSCAR',lnow)
            print('making {0}...'.format(dname))

def gather_results():
    dirs= sorted(glob.glob(_dname_prefix+"0????"))
    fo= open(_out_file,'w')
    fo.write("# encut,  vol,  e_fr,  e_en,  (e_fr - e_en) \n")
    for dir in dirs:
        if not os.path.exists(dir+"/vasprun.xml"):
            print("Erorr: "+dir+"vasprun.xml does not exist !!!")
            sys.exit()
        try:
            vasprun= Vasprun(dir+"/vasprun.xml")
            e_fr= vasprun.ionic_steps[-1]['electronic_steps'][-1]['e_fr_energy']
            e_en= vasprun.ionic_steps[-1]['electronic_steps'][-1]['eentropy']
            e_0= e_fr -e_en
            enini= vasprun.parameters['ENINI']
            enmax= vasprun.parameters['ENMAX']
            if abs(enmax-enini) > 0.1:
                print("**WARNING: ENINI and ENMAX different in vasprun.xml !!!")
            vol= vasprun.structures[-1].volume
            fo.write(" {0:7.1f} {1:10.2f} {2:15.8f} {3:15.8f} {4:15.8f}\n".format(enini,vol,e_fr,e_en,e_0))
        except:
            print("**WARNING: {0}/vasprun.xml cannot be read, and skipped...".format(dir))
    fo.close()

def replace_ENCUT(incar,encut):
    fi= open(incar,'r')
    fo= open(incar+".tmp",'w')

    text= re.compile('ENCUT')
    for line in fi.readlines():
        if text.search(line):
            fo.write('ENCUT = {0:6.1f}\n'.format(encut))
            pass
        else:
            fo.write(line)
    fi.close()
    fo.close()
    os.system('mv {0}.tmp {0}'.format(incar))

def replace_lattice_constant(poscar,lnow):
    fi= open(poscar,'r')
    fo= open(poscar+".tmp",'w')

    lines= fi.readlines()
    for il in range(len(lines)):
        line= lines[il]
        if il == 1:
            val= float(line.split()[0])
            valnew= val *lnow
            fo.write("{0:15.4f}\n".format(valnew))
        else:
            fo.write(line)
    
    fi.close()
    fo.close()
    os.system('mv {0}.tmp {0}'.format(poscar))

def energy_from_vasprun(xmlfile):
    vasprun= Vasprun(xmlfile)
    e_fr= vasprun.ionic_steps[-1]['electronic_steps'][-1]['e_fr_energy']
    e_en= vasprun.ionic_steps[-1]['electronic_steps'][-1]['eentropy']
    return e_fr, (e_fr - e_en)

if __name__ == "__main__":

    args= docopt(__doc__)

    kmin= int(args['--kmin'])
    kmax= int(args['--kmax'])
    knum= int(args['--knum'])
    emin= float(args['--emin'])
    emax= float(args['--emax'])
    enum= int(args['--enum'])
    ldiv= float(args['--ldiv'])
    lnum= int(args['--lnum'])
    prepare= args['prepare']
    gather= args['gather']
    
    if prepare:
        prepare_for_vasp(kmin,kmax,knum,emin,emax,enum,ldiv,lnum)
        print(_end_msg_prepare)
    elif gather:
        gather_results()
        print(_end_msg_gather)
