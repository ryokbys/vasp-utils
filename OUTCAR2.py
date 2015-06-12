#!/bin/env python
# -*- coding: utf-8 -*-
"""
Extracts some information such as energies and forces from OUTCAR,
and write specific output files.

USAGE:
    $ python ./OUTCAR2.py

INPUT: (these files must be in the working directory)
    - OUTCAR
"""

import os,re,commands
import optparse

#================================================== main routine
if __name__ == '__main__':
    usage= '%prog [options] OUTCAR'

    parser= optparse.OptionParser(usage=usage)
    parser.add_option("-n",dest="nion",type="int", \
                      default=None,
                      help="Number of ions..")
    parser.add_option("-s",dest="nskip",type="int", \
                      default=1,
                      help="Skip writing out every this steps.")
    (options,args)= parser.parse_args()

    infname= args[0]
    nion= options.nion
    nskip= options.nskip

    if not nion:
        print '[Error] nion is not defined.'
        print "  $ grep 'NION' OUTCAR | awk '{print $12}'"
        print '  set above digit to -n option'
        exit()

    f= open(infname,'r')

    eword='free  energy'
    fword='TOTAL-FORCE'

    nerg= commands.getoutput('grep "{0:s}" {1:s} | wc -l'.format(eword,infname))
    nfrc= commands.getoutput('grep "{0:s}" {1:s} | wc -l'.format(fword,infname))
    
    print 'nerg=',nerg
    print 'nfrc=',nfrc

    if not nerg == nfrc:
        print '[Error] nerg != nfrc !!!'
        print 'Are you OK with this? [Y/n]'
        #exit()
        ans= raw_input()
        if ans in ('n','N'):
            exit()

    nmatch= 0
    force= []
    freading= False
    for line in f.readlines():
        ematch= re.search(eword,line)
        fmatch= re.search(fword,line)
        if ematch:
            nmatch += 1
            if not nmatch % nskip == 0:
                continue
            print ' nmatch= ',nmatch
            energy= float(line.split()[4])
            ferg= open('erg.vasp.{0:05d}'.format(nmatch),'w')
            ferg.write('   {0:15.7f}\n'.format(energy))
            ferg.close()
        if fmatch: 
            if not nmatch % nskip == 0:
                continue
            freading= True
            na = 0
            ffrc= open('frc.vasp.{0:05d}'.format(nmatch),'w')
            ffrc.write('   {0:d}\n'.format(nion))
            continue
        if freading:
            if re.search('-----',line):
                continue
            na += 1
            force= [ float(x) for x in line.split()[3:6]]
            ffrc.write(' {0:10.6f}'.format(force[0]) \
                       +' {0:10.6f}'.format(force[1]) \
                       +' {0:10.6f}\n'.format(force[2]))
            if na == nion:
                freading= False
                ffrc.close()
                

    f.close()
