#!/usr/bin/ruby
#encoding: utf-8
#-----------------------------------------------------------------------
# make INCAR and KPOINTS files from POSCAR and POTCAR
#-----------------------------------------------------------------------
#.....add the directory where this file exists to the search path
$: << File.dirname(__FILE__)

require 'POSCAR.rb'
require 'POTCAR.rb'

SYSTEM= 'Si NN data'
METAL= false
SPIN_POLARIZED= false
SYMMETRY= true
OUT_INCAR_NAME='INCAR'
OUT_KPOINTS_NAME='KPOINTS'
KPOINTS_TYPE='Monkhorst-Pack' # or 'Gamma'

IBRION= -1 # -1:no update, 0:MD, 1:q-Newton, 2:CG, 3:damped MD
ISIF= 2 # 2: relax ions only, 3:shell-shape too, 4:shell volume too
NSW= 0 # number of ion relaxation steps

#...inter-point distance in k-space, usually 0.1(accurate)~0.3(loose)
KDIS= 0.2

def determine_num_kpoint(length)
  # maximum 11
  # minimum 1
  nk= (2.0*3.141592/length/KDIS).to_i
  if nk > 11 then
    return 11
  elsif nk < 1 then
    return 1
  end
  return nk
  # if length < 4.0 then
  #   return 11
  # elsif length < 6.0 then
  #   return 10
  # elsif length < 8.0 then
  #   return 8
  # elsif length < 10.0 then
  #   return 6
  # elsif length < 14.0 then
  #   return 4
  # else
  #   return 2
  # end
end

def write_KPOINTS(fname,type,ndiv)
  file=open(fname,'w')
  file.write("%dx%dx%d\n" % ndiv)
  file.write(" 0 \n")
  file.write(type+"\n")
  file.write(" %d  %d  %d\n" % ndiv)
  file.write(" %d  %d  %d\n" % [0,0,0])
  file.close
end

def write_INCAR(fname,encut,nbands)
  file= open(fname,'w')
  file.write("SYSTEM ="+SYSTEM+"\n")
  file.write("\n")
  file.write("ISTART = 1\n")
  file.write("ICHARG = 1\n")
  file.write("INIWAV = 1\n")
  if SPIN_POLARIZED then
    file.write("ISPIN  = 2\n")
    file.write("IMIX     = 4\n")
    file.write("AMIX     = 0.05\n")
    file.write("BMIX     = 0.0001\n")
    file.write("AMIX_MAG = 0.2\n")
    file.write("BMIX_MAG = 0.0001\n")
    file.write("MAXMIX   = 40\n")
  else
    file.write("ISPIN  = 1\n")
  end
  if SYMMETRY then
    file.write("ISYM   = 2\n")
  else
    file.write("ISYM   = 0\n")
  end
  file.write("\n")
  file.write("ENCUT  = %7.3f\n" % encut)
  file.write("LREAL  = Auto\n")
  file.write("EDIFF  = 1.0e-6\n")
  file.write("ALGO   = Fast\n")
  file.write("PREC   = Normal\n")
  file.write("\n")
  file.write("NELMIN = 4\n")
  file.write("NELM   = 100\n")
  file.write("NBANDS = %d\n" % nbands)
  file.write("\n")
  if METAL then
    file.write("ISMEAR = 2\n")
    file.write("SIGMA  = 0.2\n")
  else
    file.write("ISMEAR = -5\n")
    file.write("SIGMA  = 0.00001\n")
  end
  file.write("\n")
  file.write("ISIF   = %d\n" % ISIF)
  file.write("IBRION = %d\n" % IBRION) 
  file.write("POTIM  = 0.5\n") 
  file.write("SMASS  = 0.4\n") 
  file.write("NSW    = %d\n" % NSW) 
  file.write("\n")
  file.close
end

poscar= POSCAR.new()
poscar.read
potcar= read_POTCAR

encut= potcar['encut'].max
valences= potcar['valence']
a1= poscar.a1
a2= poscar.a2
a3= poscar.a3
al= poscar.afac
natms= poscar.num_atoms

ntot= 0
nele= 0
natms.length.times do |i|
  ntot= ntot +natms[i]
  nele= nele +natms[i]*valences[i].to_i
end
if SPIN_POLARIZED then
  nbands= (nele/2 *1.8).to_i
else
  nbands= (nele/2 *1.4).to_i
end
if nbands < 50 then
  nbands= nele
end

l1= al*Math.sqrt(a1[0]**2 +a1[1]**2 +a1[2]**2)
l2= al*Math.sqrt(a2[0]**2 +a2[1]**2 +a2[2]**2)
l3= al*Math.sqrt(a3[0]**2 +a3[1]**2 +a3[2]**2)
k1= determine_num_kpoint(l1)
k2= determine_num_kpoint(l2)
k3= determine_num_kpoint(l3)
ndiv= [k1,k2,k3]

write_KPOINTS(OUT_KPOINTS_NAME,KPOINTS_TYPE,ndiv)
write_INCAR(OUT_INCAR_NAME,encut,nbands)
