#!/bin/env python

import numpy as np
import optparse

def read_EIGENVAL(fname="EIGENVAL"):
    f= open(fname,'r')
    buffer= f.readline().split()
    nspin= int(buffer[3])
    #...skip lines
    f.readline() #2
    f.readline() #3
    f.readline() #4
    f.readline() #5
    buffer= f.readline().split()
    nelect= int(buffer[0])
    nkpts= int(buffer[1])
    nbands= int(buffer[2])
    f.readline() # empty line
    kpts= np.zeros([nkpts,4])
    evs= np.zeros([nkpts,nbands,nspin])

    for ik in range(nkpts):
        buffer=f.readline().split()
        kpts[ik,0]= float(buffer[0])
        kpts[ik,1]= float(buffer[1])
        kpts[ik,2]= float(buffer[2])
        for ib in range(nbands):
            buffer= f.readline().split()
            if nspin == 1:
                evs[ik,ib,0]= float(buffer[1])
            elif nspin == 2:
                evs[ik,ib,0]= float(buffer[1])
                evs[ik,ib,1]= float(buffer[2])
        buffer=f.readline() # empty line
    f.close()
    return nelect,nkpts,nbands,kpts,evs


if __name__ == "__main__":

    usage= 'python %prog [options] [EIGENVAL]'

    parser= optparse.OptionParser(usage=usage)
    parser.add_option("-e",dest="efermi",type="float",default=0.0,
                      help="Fermi level to be shifted for this band.")
    (options,args)= parser.parse_args()

    ef= options.efermi
    evfname='EIGENVAL'
    if len(args) != 0:
        evfname= args[0]

    nelect,nkpts,nbands,kpts,evs= read_EIGENVAL(evfname)
    
    fo= open('out.band','w')
    for ik in range(nkpts):
        fo.write(' {0:3d} '.format(ik))
        for ib in range(nbands):
            fo.write(' {0:15.7f}'.format((evs[ik,ib,0]-ef)))
        fo.write('\n')
    fo.close()
    print 'out.band was written.'

    fg= open('gp.band','w')
    str="""unset key
set xl 'Wave number'
set yl 'Energy (eV)'
unset xtics
"""
    fg.write(str)
    fg.write('plot ')
    for ib in range(nbands):
        fg.write(" 'out.band' us 1:{0:d} w l".format(ib+2))
        if ib != nbands -1:
            fg.write(',')
    fg.write('\n')
    fg.close()
    print 'gp.band was written.'
