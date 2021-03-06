import numpy as np
import math
import sys
import copy

from Atom import Atom

#...constants
_maxnn= 40
_max_species= 9

class AtomSystem(object):
    u"""
    AtomSystem has cell information and atoms.
    """

    def __init__(self):
        self.a1= np.zeros(3)
        self.a2= np.zeros(3)
        self.a3= np.zeros(3)
        self.atoms= []

    def set_lattice(self,alc,a1,a2,a3):
        self.alc= alc
        self.a1= a1
        self.a2= a2
        self.a3= a3

    def add_atom(self,atom):
        self.atoms.append(atom)

    def reset_ids(self):
        for i in range(len(self.atoms)):
            ai= self.atoms[i]
            ai.set_id(i+1)

    def num_atoms(self):
        return len(self.atoms)

    def read_pmd(self,fname='pmd0000'):
        f=open(fname,'r')
        # 1st: lattice constant
        self.alc= float(f.readline().split()[0])
        # 2nd-4th: cell vectors
        self.a1= np.array([float(x) for x in f.readline().split()])
        self.a2= np.array([float(x) for x in f.readline().split()])
        self.a3= np.array([float(x) for x in f.readline().split()])
        # 5th-7th: velocity of cell vectors
        tmp= f.readline().split()
        tmp= f.readline().split()
        tmp= f.readline().split()
        # 8st: num of atoms
        buff= f.readline().split()
        natm= int(buff[0])
        nauxd= 9
        # 9th-: atom positions
        self.atoms= []
        for i in range(natm):
            data= [float(x) for x in f.readline().split()]
            ai= Atom()
            ai.decode_tag(data[0])
            ai.set_pos(data[1],data[2],data[3])
            ai.set_auxd(data[4:4+nauxd])
            self.atoms.append(ai)
        f.close()

    def write_pmd(self,fname='pmd0000'):
        f=open(fname,'w')
        # lattice constant
        f.write(" {0:15.7f}\n".format(self.alc))
        # cell vectors
        f.write(" {0:15.7f} {1:15.7f} {2:15.7f}\n".format(self.a1[0],\
                                                          self.a1[1],\
                                                          self.a1[2]))
        f.write(" {0:15.7f} {1:15.7f} {2:15.7f}\n".format(self.a2[0],\
                                                          self.a2[1],\
                                                          self.a2[2]))
        f.write(" {0:15.7f} {1:15.7f} {2:15.7f}\n".format(self.a3[0],\
                                                          self.a3[1],\
                                                          self.a3[2]))
        # velocities of cell vectors
        f.write(" {0:15.7f} {1:15.7f} {2:15.7f}\n".format(0.0, 0.0, 0.0))
        f.write(" {0:15.7f} {1:15.7f} {2:15.7f}\n".format(0.0, 0.0, 0.0))
        f.write(" {0:15.7f} {1:15.7f} {2:15.7f}\n".format(0.0, 0.0, 0.0))
        # num of atoms
        f.write(" {0:10d}\n".format(len(self.atoms)))
        # atom positions
        for i in range(len(self.atoms)):
            ai= self.atoms[i]
            ai.set_id(i+1)
            f.write(" {0:22.14e} {1:11.7f} {2:11.7f} {3:11.7f}".format(ai.tag(), \
                                                            ai.pos[0],\
                                                            ai.pos[1],\
                                                            ai.pos[2])
                    +"  {0:.1f}  {1:.1f}  {2:.1f}".format(0.0, 0.0, 0.0)
                    +"  {0:.1f}  {1:.1f}".format(0.0, 0.0)
                    +"  {0:.1f}  {1:.1f}  {2:.1f}".format(0.0, 0.0, 0.0)
                    +"  {0:.1f}  {1:.1f}  {2:.1f}".format(0.0, 0.0, 0.0)
                    +"  {0:.1f}  {1:.1f}  {2:.1f}".format(0.0, 0.0, 0.0)
                    +"\n")
        f.close()

    def read_akr(self,fname='akr0000'):
        f=open(fname,'r')
        # 1st: lattice constant
        self.alc= float(f.readline().split()[0])
        # 2nd-4th: cell vectors
        self.a1= np.array([float(x) for x in f.readline().split()])
        self.a2= np.array([float(x) for x in f.readline().split()])
        self.a3= np.array([float(x) for x in f.readline().split()])
        # 5th: num of atoms
        buff= f.readline().split()[0]
        natm= int(buff[0])
        nauxd= int(buff[1])
        if nauxd < 3:
            print '[Error] read_akr(): nauxd < 3 !!!'
            sys.exit()
        # 9th-: atom positions
        self.atoms= []
        for i in range(natm):
            data= [float(x) for x in f.readline().split()]
            ai= Atom()
            ai.set_sid(data[0])
            ai.set_pos(data[1],data[2],data[3])
            # if there are less than 3 auxiliary data, there is not velocity
            ai.set_vel(data[4],data[5],data[6])
            self.atoms.append(ai)
        f.close()

    def write_akr(self,fname='akr0000'):
        f=open(fname,'w')
        # lattice constant
        f.write(" {0:12.4f}\n".format(self.alc))
        # cell vectors
        f.write(" {0:12.4f} {1:12.4f} {2:12.4f}\n".format(self.a1[0],\
                                                          self.a1[1],\
                                                          self.a1[2]))
        f.write(" {0:12.4f} {1:12.4f} {2:12.4f}\n".format(self.a2[0],\
                                                          self.a2[1],\
                                                          self.a2[2]))
        f.write(" {0:12.4f} {1:12.4f} {2:12.4f}\n".format(self.a3[0],\
                                                          self.a3[1],\
                                                          self.a3[2]))
        # num of atoms
        f.write(" {0:10d} {1:4d} {2:4d} {3:4d}\n".format(len(self.atoms),3,0,0))
        # atom positions
        for i in range(len(self.atoms)):
            ai= self.atoms[i]
            ai.set_id(i+1)
            f.write(" {0:4d} {1:10.5f} {2:10.5f} {3:10.5f}".format(ai.sid, \
                                                            ai.pos[0],\
                                                            ai.pos[1],\
                                                            ai.pos[2])
                    +"  {0:12.4e}  {1:12.4e}  {2:12.4e}".format(ai.vel[0],\
                                                                ai.vel[1],\
                                                                ai.vel[2])
                    +"\n")
        f.close()

    def read_POSCAR(self,fname='POSCAR'):
        f=open(fname,'r')
        # 1st: comment
        self.c1= f.readline()
        # 2nd: multiplying factor
        self.alc= float(f.readline().split()[0])
        # 3-5: lattice vectors
        self.a1= np.array([float(x) for x in f.readline().split()])
        self.a2= np.array([float(x) for x in f.readline().split()])
        self.a3= np.array([float(x) for x in f.readline().split()])
        # 6th: num of atoms par species
        data= f.readline().split()
        if( data[0].isdigit() ):
            natm_per_spcs= np.array([int(d) for d in data])
        else:
            # skip one line and read next line
            data= f.readline().split()
            natm_per_spcs= np.array([int(d) for d in data])
        # 7th: comment (in some cases, 8th line too)
        self.c7= f.readline()
        if self.c7[0] in ('s','S'):
            self.c8= f.readline()
        # hereafter: atom positions
        sid= 0
        self.atoms=[]
        for ni in natm_per_spcs:
            sid += 1
            for j in range(ni):
                line= f.readline().split()
                data= [ float(line[i]) for i in range(3)]
                ai= Atom()
                ai.set_sid(sid)
                ai.set_pos(data[0],data[1],data[2])
                ai.set_auxd(line[3:])
                ai.pbc()
                self.atoms.append(ai)
        f.close()

    def write_POSCAR(self,fname='POSCAR'):
        f= open(fname,'w')
        if hasattr(self,'c1'):
            f.write(self.c1)
        else:
            f.write('Written by AtomSystem.py\n')
        f.write(' {0:13.8f}\n'.format(self.alc))
        f.write(' {0:13.8f} {1:13.8f} {2:13.8f}\n'.format(self.a1[0],
                                                          self.a1[1],
                                                          self.a1[2]))
        f.write(' {0:13.8f} {1:13.8f} {2:13.8f}\n'.format(self.a2[0],
                                                          self.a2[1],
                                                          self.a2[2]))
        f.write(' {0:13.8f} {1:13.8f} {2:13.8f}\n'.format(self.a3[0],
                                                          self.a3[1],
                                                          self.a3[2]))
        # count species in the system
        natm_per_spcs=[ 0 for i in range(_max_species)]
        for ai in self.atoms:
            natm_per_spcs[ai.sid-1] += 1
        for i in range(_max_species):
            if natm_per_spcs[i] != 0:
                f.write(' {0:3d}'.format(natm_per_spcs[i]))
        f.write('\n')

        if hasattr(self,'c7'):
            f.write(self.c7)
        else:
            f.write('Direct\n')
        if hasattr(self,'c8'):
            f.write(self.c8)

        for ai in self.atoms:
            f.write(' {0:13.8f} {1:13.8f} {2:13.8f} '.format(ai.pos[0],\
                                                             ai.pos[1],\
                                                             ai.pos[2]) )
            for aux in ai.auxd:
                f.write(' {0}'.format(aux))
            f.write('\n')
        f.close()

    def make_pair_list(self,rcut=3.0):
        rc2= rcut**2
        h= np.zeros((3,3))
        h[0]= self.a1 *self.alc
        h[1]= self.a2 *self.alc
        h[2]= self.a3 *self.alc
        hi= np.linalg.inv(h)
        print h
        print hi
        lcx= int(1.0/math.sqrt(hi[0,0]**2 +hi[0,1]**2 +hi[0,2]**2)/rcut)
        lcy= int(1.0/math.sqrt(hi[1,0]**2 +hi[1,1]**2 +hi[1,2]**2)/rcut)
        lcz= int(1.0/math.sqrt(hi[2,0]**2 +hi[2,1]**2 +hi[2,2]**2)/rcut)
        if lcx == 0: lcx= 1
        if lcy == 0: lcy= 1
        if lcz == 0: lcz= 1
        lcyz= lcy*lcz
        lcxyz= lcx*lcy*lcz
        rcx= 1.0/lcx
        rcy= 1.0/lcy
        rcz= 1.0/lcz
        rcxi= 1.0/rcx
        rcyi= 1.0/rcy
        rczi= 1.0/rcz
        lscl= np.zeros((len(self.atoms),),dtype=int)
        lshd= np.zeros((lcxyz,),dtype=int)
        lscl[:]= -1
        lshd[:]= -1
        print 'lcx,lcy,lcz=',lcx,lcy,lcz
        print 'rcx,rcy,rcz=',rcx,rcy,rcz

        #...make a linked-cell list
        for i in range(len(self.atoms)):
            pi= self.atoms[i].pos
            #...assign a vector cell index
            mx= int(pi[0]*rcxi)
            my= int(pi[1]*rcyi)
            mz= int(pi[2]*rczi)
            m= mx*lcyz +my*lcz +mz
            # print i,mx,my,mz,m
            lscl[i]= lshd[m]
            lshd[m]= i

        #...make a pair list
        self.nlspr= np.zeros((self.num_atoms(),),dtype=int)
        self.lspr= np.zeros((self.num_atoms(),_maxnn),dtype=int)
        self.lspr[:]= -1
        # self.lspr= []
        # for i in range(len(self.atoms)):
        #     self.lspr.append([])
            
        for ia in range(len(self.atoms)):
            if ia % 10000 == 0:
                print 'ia=',ia
            ai= self.atoms[ia]
            pi= ai.pos
            mx= int(pi[0]*rcxi)
            my= int(pi[1]*rcyi)
            mz= int(pi[2]*rczi)
            m= mx*lcyz +my*lcz +mz
            #print 'ia,pi,mx,my,mz,m=',ia,pi[0:3],mx,my,mz,m
            for kuz in range(-1,2):
                m1z= mz +kuz
                if m1z < 0: m1z += lcz
                if m1z >= lcz: m1z -= lcz
                for kuy in range(-1,2):
                    m1y= my +kuy
                    if m1y < 0: m1y += lcy
                    if m1y >= lcy: m1y -= lcy
                    for kux in range(-1,2):
                        m1x= mx +kux
                        if m1x < 0: m1x += lcx
                        if m1x >= lcx: m1x -= lcx
                        m1= m1x*lcyz +m1y*lcz +m1z
                        ja= lshd[m1]
                        if ja== -1: continue
                        self.scan_j_in_cell(ia,pi,ja,lscl,h,rc2)
        #...after makeing lspr
        # for ia in range(len(self.atoms)):
        #     print ia,self.lspr[ia]

    def scan_j_in_cell(self,ia,pi,ja,lscl,h,rc2):
        if ja == ia: ja = lscl[ja]
        if ja == -1: return 0
        aj= self.atoms[ja]
        pj= aj.pos
        xij= pj-pi
        xij[0] =self.pbc(xij[0])
        xij[1] =self.pbc(xij[1])
        xij[2] =self.pbc(xij[2])
        rij= np.dot(h,xij)
        rij2= rij[0]**2 +rij[1]**2 +rij[2]**2
        if rij2 < rc2:
            n= self.nlspr[ia]
            self.lspr[ia,n]= ja
            self.nlspr[ia] += 1
            if self.nlspr[ia] >= _maxnn:
                print ' [Error] self.nlspr[{0}] >= _maxnn !!!'.format(ia)
                sys.exit()
        ja= lscl[ja]
        self.scan_j_in_cell(ia,pi,ja,lscl,h,rc2)

    def pbc(self,x):
        if x <= -0.5:
            return x +1.0
        elif x >   0.5:
            return x -1.0
        else:
            return x

    def expand(self,n1,n2,n3):
        #...expand unit vectors
        self.a1= self.a1*n1
        self.a2= self.a2*n2
        self.a3= self.a3*n3
        n123= n1*n2*n3
        nsid= 0
        for ai in self.atoms:
            nsid= max(nsid,ai.sid)
        natm_per_spcs= np.zeros((nsid,),dtype=int)
        for ai in self.atoms:
            sid= ai.sid -1
            natm_per_spcs[sid] += 1
        natm0= self.num_atoms()
        atoms0= copy.copy(self.atoms)
        self.atoms= []
        aid= 0
        for ai0 in atoms0:
            ai0.pos[0] /= n1
            ai0.pos[1] /= n2
            ai0.pos[2] /= n3
            for i1 in range(n1):
                for i2 in range(n2):
                    for i3 in range(n3):
                        aid += 1
                        ai= Atom()
                        ai.sid= ai0.sid
                        x= ai0.pos[0]+1.0/n1*i1
                        y= ai0.pos[1]+1.0/n2*i2
                        z= ai0.pos[2]+1.0/n3*i3
                        ai.set_pos(x,y,z)
                        ai.set_auxd(ai0.auxd)
                        ai.set_id(aid)
                        self.atoms.append(ai)
