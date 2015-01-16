#!/opt/local/bin/python
"""
Calculate elastic constants, C11, C12, C44,
Young's modulus, poison's ratio, and shear modulus,
by static method which measures energy differences
w.r.t. given strains.
"""

import sys,os,commands
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#...constants
niter= 10
dltmax= 0.01
outfname='out.elastic-constants'
graphname='graph.elastic-constants.eps'

def read_POSCAR(fname='POSCAR'):
    f=open(fname,'r')
    #...1st line: comment
    cmmt= f.readline()
    #...read 1st line and get current lattice size
    al= float(f.readline().split()[0])
    hmat= np.zeros((3,3))
    hmat[0]= [ float(x) for x in f.readline().split() ]
    hmat[1]= [ float(x) for x in f.readline().split() ]
    hmat[2]= [ float(x) for x in f.readline().split() ]
    natm= int(f.readline().split()[0])
    f.close()
    return (al,hmat,natm)

def get_vol(al,hmat):
    a1= hmat[0:3,0] *al
    a2= hmat[0:3,1] *al
    a3= hmat[0:3,2] *al
    return np.dot(a1,np.cross(a2,a3))

def replace_hmat(hmat,fname='POSCAR'):
    f=open(fname,'r')
    ini= f.readlines()
    f.close()
    g=open(fname,'w')
    for l in range(len(ini)):
        if l in (2,3,4): #...hmat lines
            g.write(' {0:15.7f}'.format(hmat[l-2,0]))
            g.write(' {0:15.7f}'.format(hmat[l-2,1]))
            g.write(' {0:15.7f}'.format(hmat[l-2,2]))
            g.write('\n')
        else:
            g.write(ini[l])
    g.close()

def quad_func(x,a,b):
    return a *x**2 +b

if __name__ == '__main__':
    
    if len(sys.argv) != 1:
        print ' [Error] number of arguments wrong !!!'
        print '  Usage: $ {0}'.format(sys.argv[0])
        sys.exit()

    al,hmat0,natm= read_POSCAR()
    hmax= np.max(hmat0)

    outfile1= open(outfname,'w')
    #...get reference energy
    os.system('vasp > out.vasp')
    erg0= float(commands.getoutput("tail -n1 OSZICAR | awk '{print $5}'"))
    #erg0= float(commands.getoutput("grep 'potential energy' out.pmd | head -n1 | awk '{print $3}'"))
    print ' {0:10.4f} {1:15.7f} {2:15.7f} {3:15.7f}'.format(0.0,erg0,erg0,erg0)
    outfile1.write(' {0:10.4f} {1:15.7f} {2:15.7f} {3:15.7f}\n'.format(0.0,erg0,erg0,erg0))
    ddlt= dltmax/niter
    for iter in range(niter):
        dlt= (ddlt*(iter+1))
        dh= hmax*dlt
        #...uniaxial strain for calc C11
        hmat= np.copy(hmat0)
        hmat[0,0]= hmat[0,0] +dh
        replace_hmat(hmat)
        os.system('vasp > out.vasp')
        #erg11= float(commands.getoutput("grep 'potential energy' out.pmd | head -n1 | awk '{print $3}'"))
        erg11= float(commands.getoutput("tail -n1 OSZICAR | awk '{print $5}'"))
        #...orthorhombic volume-conserving strain for (C11-C12)
        hmat= np.copy(hmat0)
        hmat[0,0]= hmat[0,0] +dh
        hmat[1,1]= hmat[1,1] -dh
        hmat[2,2]= hmat[2,2] +dh**2/(1.0-dh**2)
        replace_hmat(hmat)
        os.system('vasp > out.vasp')
        #erg12= float(commands.getoutput("grep 'potential energy' out.pmd | head -n1 | awk '{print $3}'"))
        erg12= float(commands.getoutput("tail -n1 OSZICAR | awk '{print $5}'"))
        #...monoclinic volume-conserving strain for C44
        hmat= np.copy(hmat0)
        hmat[0,1]= hmat[0,1] +dh/2
        hmat[1,0]= hmat[1,0] +dh/2
        hmat[2,2]= hmat[2,2] +dh**2/(4.0-dh**2)
        replace_hmat(hmat)
        os.system('vasp > out.vasp')
        #erg44= float(commands.getoutput("grep 'potential energy' out.pmd | head -n1 | awk '{print $3}'"))
        erg44= float(commands.getoutput("tail -n1 OSZICAR | awk '{print $5}'"))
        print ' {0:10.4f} {1:15.7f} {2:15.7f} {3:15.7f}'.format(dlt,erg11,erg12,erg44)
        outfile1.write(' {0:10.4f} {1:15.7f} {2:15.7f} {3:15.7f}\n'.format(dlt,erg11,erg12,erg44))
    outfile1.close()

    #...revert POSCAR
    replace_hmat(hmat0)

    #...prepare for Murnaghan fitting
    f= open(outfname,'r')
    lines= f.readlines()
    dlts= np.zeros((len(lines)))
    e11s= np.zeros((len(lines)))
    e12s= np.zeros((len(lines)))
    e44s= np.zeros((len(lines)))
    for l in range(len(lines)):
        dat= lines[l].split()
        dlts[l]= float(dat[0])
        e11s[l]= float(dat[1])
        e12s[l]= float(dat[2])
        e44s[l]= float(dat[3])
    f.close()

    #...set initial values
    a= 1.0
    b= erg0
    p0= np.array([a,b])
    vol= get_vol(al,hmat0)
    #...least square fitting
    popt11,pcov11= curve_fit(quad_func,dlts,e11s,p0=p0)
    popt12,pcov12= curve_fit(quad_func,dlts,e12s,p0=p0)
    popt44,pcov44= curve_fit(quad_func,dlts,e44s,p0=p0)

    c11= popt11[0]/vol*2 *160.2
    c11_c12= popt12[0]/vol *160.2
    c12= c11 -c11_c12
    c44= popt44[0]/vol*2 *160.2

    #...output results
    print '{0:=^72}'.format(' RESULTS ')
    print ' C11     = {0:10.3f} GPa'.format(c11)
    print ' C11-C12 = {0:10.3f} GPa'.format(c11_c12)
    print ' C12     = {0:10.3f} GPa'.format(c12)
    print ' C44     = {0:10.3f} GPa'.format(c44)
    ymod= c44*(2.0*c44+3.0*c12)/(c11+c44)
    prto= c12/2.0/(c11+c44)
    smod= ymod/2.0/(1.0+prto)
    print ' Following values maybe only valid for isotropic materials...'
    print ' Young\'s modulus = {0:10.3f} GPa'.format(ymod)
    print ' Poisson\'s ratio = {0:10.3f}'.format(prto)
    print ' shear modulus   = {0:10.3f} GPa'.format(smod)
    
    plt.plot(dlts,quad_func(dlts,*popt11),dlts,e11s,'o')
    plt.plot(dlts,quad_func(dlts,*popt12),dlts,e12s,'o')
    plt.plot(dlts,quad_func(dlts,*popt44),dlts,e44s,'o')
    plt.title('Energy vs. strain')
    plt.legend(['C11 fitted','C11 data'
                ,'C12 fitted','C12 data'
                ,'C44 fitted','C44 data'],loc=2)
    plt.xlabel('Strain')
    plt.ylabel('Energy (eV)')
    plt.savefig(graphname,dpi=150)
    plt.show()

    print '{0:=^72}'.format(' OUTPUT ')
    print ' * '+outfname
    print ' * '+graphname
