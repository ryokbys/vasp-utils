#!/bin/env python
"""
Make appropriate INCAR and kPOINTS files for VASP calculation
from POSCAR and POTCAR files. Number of division in each k-space direction
must be set, otherwise default NORMAL accuracy setting will be chosen.
"""

import math,optparse
import POSCAR,POTCAR

_usage= '%prog [options]'


_version='0.1a'
_SYSTEM='system made by prepare-vasp.py '+ _version
_metal= False
_spin_polarized= False
_symmetry= True
_INCAR_name= 'INCAR'
_KPOINTS_name= 'KPOINTS'
_KPOINTS_type= 'Monkhorst-Pack' # or 'Gamma'

_IBRION= -1  # -1:no update, 0:MD, 1:q-Newton, 2:CG, 3:damped MD
_ISIF= 2 # 2: relax ions only, 3:shell-shape too, 4:shell volume too
_NSW= 0 # number of ion relaxation steps

def determine_num_kpoint(b_length,pitch,leven):
    # maximum 11
    # minimum 1
    nk= int(2.0 *math.pi /b_length /pitch)
    if nk > 11:
        return 11
    elif nk < 1:
        return 1
    if leven:
        if nk % 2 == 1:
            nk= nk +1
    else:
        if nk % 2 == 0:
            nk= nk +1
    return nk

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
    
    file.close()

if __name__ == '__main__':

    parser= optparse.OptionParser(usage=_usage)
    parser.add_option("-p","--pitch",
                      dest="pitch",
                      type="float",
                      default=0.2,
                      help="pitch of k in a direction.")
    parser.add_option("-e","--even",
                      action="store_true",
                      dest="leven",
                      default=False,
                      help="flag to set number of k-points in a direction even.")

    (options,args)= parser.parse_args()

    pitch= options.pitch
    leven= options.leven

    print ' Pitch of k points = {0:5.1f}'.format(pitch)

    poscar= POSCAR.POSCAR()
    poscar.read()
    
    potcar= POTCAR.read_POTCAR()
    encut= max(potcar['encut'])
    valences= potcar['valence']
    a1= poscar.h[:,0]
    a2= poscar.h[:,1]
    a3= poscar.h[:,2]
    al= poscar.afac
    natms= poscar.num_atoms

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

    l1= al *math.sqrt(a1[0]**2 +a1[1]**2 +a1[2]**2)
    l2= al *math.sqrt(a2[0]**2 +a2[1]**2 +a2[2]**2)
    l3= al *math.sqrt(a3[0]**2 +a3[1]**2 +a3[2]**2)
    print ' Length of each axes:'
    print '   l1 = {0:10.3f}'.format(l1)
    print '   l2 = {0:10.3f}'.format(l2)
    print '   l3 = {0:10.3f}'.format(l3)
    k1= determine_num_kpoint(l1,pitch,leven)
    k2= determine_num_kpoint(l2,pitch,leven)
    k3= determine_num_kpoint(l3,pitch,leven)
    print ' Number of k-points: {0:2d} {1:2d} {2:2d}'.format(k1,k2,k3)
    ndiv= [k1,k2,k3]
    
    write_KPOINTS(_KPOINTS_name,_KPOINTS_type,ndiv)
    write_INCAR(_INCAR_name,encut,nbands)
