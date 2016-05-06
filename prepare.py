#!/bin/env python
"""
Make appropriate INCAR and kPOINTS files for VASP calculation
from POSCAR and POTCAR files. Number of division in each k-space direction
must be set, otherwise default NORMAL accuracy setting will be chosen.

Usage:
  prepare.py [options]

Options:
  -h, --help  Show this help and exit.
  -p, --pitch=PITCH
              Pitch of k in each direction in A^{-1}. [default: 0.1]
  --pot-dir=POTDIR
              Directory path where vasp potentials are. [default "~/local/vasp/potpaw_PBE"]
"""

from docopt import docopt
import math
import poscar, potcar
import numpy as np


__author__  = 'Ryo KOBAYASHI'
__version__ = '160115'
__license__ = 'MIT'

_SYSTEM='system made by prepare-vasp.py '+ _version
_metal= False
_spin_polarized= False
_symmetry= False
_INCAR_name= 'INCAR'
_KPOINTS_name= 'KPOINTS'
_KPOINTS_type= 'Monkhorst-Pack' # or 'Gamma'

_IBRION= -1  # -1:no update, 0:MD, 1:q-Newton, 2:CG, 3:damped MD
_ISIF= 2 # 2: relax ions only, 3:shell-shape too, 4:shell volume too
_NSW= 0 # number of ion relaxation steps

_NPAR= 4

_defaults ={'SYSTEM': ' system made via prepare-vasp.py'+_version,
            'ISYM': ' 2',
            'ISPIN': ' 2',
            'IBRION': ' -1',
            'ISIF': ' 2',
            'NSW': ' 0',
            'NPAR': ' 4',
}
_comments ={'ISTART': ' # startjob [0:no 1:use WAVECAR 2:samecut]',
            'ICHARG': ' # charge [1:use CHGCAR 2:from atoms 10:const.]'
            'PREC': ' # precession [medium/high/low/normal/accurate]',
            'ISPIN': ' # spin [1:non-polarized 2:polarized]',
            'INIWAV': ' # initial electr wf. [0:lowe 1:randlectr(default)]',
            'NPAR': ' # parallelization (default: total num of nodes)',
            'NWRITE': ' # write-flag & timer',
            'LWAVE': ' # eigenvalues on WAVECAR',
            'LCHARG': ' # create CHGCAR',
            'LVTOT': ' # write LOCPOT, local potential',
            'NBAND': ' # numer of bands to be computed',
            'MAGMOM': ' # magnetic moment',
            'ENCUT': ' # energy cutoff in eV',
            'EDIFF': ' # stopping-criterion for electronic update',
            'NSW': ' # number of io relaxation steps',
            'ISIF': ' # 2: relax ions only, 3:shell-shape too, 4:shell volume too',
            'IBRION': ' # -1:no update, 0:MD, 1:q-Newton, 2:CG, 3:damped MD',
}

def norm(vec):
    v2= np.dot(vec,vec)
    return np.sqrt(v2)

def get_kpts(cell,pitch=0.1):
    a1= cell[0]; a2= cell[1]; a3= cell[2]
    b1= 2.0*np.pi *np.cross(a2,a3)/ np.dot(a1,np.cross(a2,a3))
    b2= 2.0*np.pi *np.cross(a3,a1)/ np.dot(a2,np.cross(a3,a1))
    b3= 2.0*np.pi *np.cross(a1,a2)/ np.dot(a3,np.cross(a1,a2))
    bb1= norm(b1); bb2= norm(b2); bb3= norm(b3)
    kpts= (int(bb1/pitch),int(bb2/pitch),int(bb3/pitch))
    return kpts

def write_KPOINTS(fname,type,ndiv):
    f=open(fname,'w')
    f.write('{0:d}x{1:d}x{1:d}\n'.format(ndiv[0],ndiv[1],ndiv[2]))
    f.write('0\n')
    f.write(type+'\n')
    f.write(' {0:2d} {1:2d} {2:2d}\n'.format(ndiv[0],ndiv[1],ndiv[2]))
    f.write(' {0:2d} {1:2d} {2:2d}\n'.format(0,0,0))
    f.close()

def write_INCAR(fname,encut,nbands):
    file=open(fname,'w')
    file.write("SYSTEM ="+_SYSTEM+"\n")
    file.write("\n")
    file.write("ISTART = 1\n")
    file.write("ICHARG = 1\n")
    file.write("INIWAV = 1\n")
    if _spin_polarized:
        file.write("ISPIN  = 2\n")
        file.write("IMIX     = 4\n")
        file.write("AMIX     = 0.05\n")
        file.write("BMIX     = 0.0001\n")
        file.write("AMIX_MAG = 0.2\n")
        file.write("BMIX_MAG = 0.0001\n")
        file.write("MAXMIX   = 40\n")
    else:
        file.write("ISPIN  = 1\n")

    if _symmetry:
        file.write("ISYM   = 2\n")
    else:
        file.write("ISYM   = 0\n")

    file.write("\n")
    file.write("ENCUT  = {0:7.3f}\n".format(encut))
    file.write("LREAL  = Auto\n")
    file.write("EDIFF  = 1.0e-6\n")
    file.write("ALGO   = Fast\n")
    file.write("PREC   = Normal\n")
    file.write("\n")
    file.write("NELMIN = 4\n")
    file.write("NELM   = 100\n")
    file.write("NBANDS = {0:4d}\n".format(nbands))
    file.write("\n")
    if _metal:
        file.write("ISMEAR = 2\n")
        file.write("SIGMA  = 0.2\n")
    else:
        file.write("ISMEAR = -5\n")
        file.write("SIGMA  = 0.00001\n")

    file.write("\n")
    file.write("ISIF   = {0:2d}\n".format(_ISIF))
    file.write("IBRION = {0:2d}\n".format(_IBRION))
    file.write("POTIM  = 0.5\n") 
    file.write("SMASS  = 0.4\n") 
    file.write("NSW    = {0:4d}\n".format(_NSW))
    file.write("\n")
    
    file.write("NPAR   = {0:4d}\n".format(_NPAR)) 
    file.write("\n")
    
    file.close()

if __name__ == '__main__':


    args= docopt(__doc__)
    pitch= float(args['--pitch'])
    dpath= args['--pot-dir']
    dpath= os.path.expanduser(dpath)

    print ' Pitch of k points = {0:5.1f}'.format(pitch)

    posc= poscar.POSCAR()
    posc.read()
    
    potc= potcar.read_POTCAR()
    species= potc['species']
    encut= max(potc['encut'])
    valences= potc['valence']
    a1= posc.h[:,0]
    a2= posc.h[:,1]
    a3= posc.h[:,2]
    al= posc.afac
    cell = [a1*al,a2*al,a3*al]
    natms= posc.num_atoms

    print " species:",species
    print " encut:",encut
    print " valences:",valences
    print " natms:",natms
    ntot= 0
    nele= 0
    for i in range(len(natms)):
        ntot= ntot +natms[i]
        nele= nele +natms[i]*int(valences[i])
    
    if _spin_polarized:
        nbands= int(nele/2 *1.8)
    else:
        nbands= int(nele/2 *1.4)
    
    if nbands < 50:
        nbands= nele

    kpts= get_kpts(cell,pitch)
    
    write_KPOINTS(_KPOINTS_name,_KPOINTS_type,kpts)
    write_INCAR(_INCAR_name,encut,nbands)
