#!/usr/bin/ruby
#
# Convert POSCAR file to pmd-format file
#
# Usage:
#   $ ./POSCAR2pmd.rb > pmd00000-0000
# Input:
#   - POSCAR
#   - OUTCAR?
#

#.....add the directory where this file exists to the search path
$: << File.dirname(__FILE__)

require 'MD_classes.rb'

#AA2BOHR= 1.88972616356
AA2BOHR= 1.0/0.5291772

def read_POSCAR(filename="./POSCAR")
  file= open(filename)
  #.....1st line: comment
  $c1=file.gets
  #.....2nd line: multiply factor
  $afac= file.gets.to_f
  #.....3rd-5th lines: lattice vectors
  a1=[]
  i=0
  (file.gets.split).each do |a|
    a1[i]= $afac *a.to_f 
    i += 1
  end
  a2=[]
  i=0
  (file.gets.split).each do |a|
    a2[i]= $afac *a.to_f
    i += 1
  end
  a3=[]
  i=0
  (file.gets.split).each do |a|
    a3[i]= $afac *a.to_f
    i += 1
  end
  $system= MD_system.new(a1,a2,a3)
  #.....6th line: num of atoms
  nums=[]
  i=0
  (file.gets.split).each do |n|
    nums[i]= n.to_i
    i += 1
  end
  #.....7th line: comment
  $c7= file.gets
  #.....8th--: atom positions
  pos=[]
  sid=0
  nums.each do |n|
    sid += 1
    (0..n-1).each do |j|
      pos= file.gets.split
      atom= MD_atom.new(pos[0].to_f, pos[1].to_f, pos[2].to_f, sid)
      $system.add_atom(atom)
    end
  end
  file.close
#  p afac
#  p a1
#  p a2
#  p a3
end

def species2tag(isp,id)
  return isp +0.1 +1e-14*id
end

def out_pmd
  printf(" %6d\n",$system.natm)
  a1= $system.a1
  a2= $system.a2
  a3= $system.a3
  (0..2).each do |i|
    a1[i] *= AA2BOHR
    a2[i] *= AA2BOHR
    a3[i] *= AA2BOHR
  end
  printf(" %12.7f %12.7f %12.7f\n", a1[0],a1[1],a1[2])
  printf(" %12.7f %12.7f %12.7f\n", a2[0],a2[1],a2[2])
  printf(" %12.7f %12.7f %12.7f\n", a3[0],a3[1],a3[2])
  printf(" %12.7f %12.7f %12.7f\n", 0.0,0.0,0.0)
  printf(" %12.7f %12.7f %12.7f\n", 0.0,0.0,0.0)
  printf(" %12.7f %12.7f %12.7f\n", 0.0,0.0,0.0)
  $system.natm.times do |i|
    atom= $system.atoms[i]
    printf("%22.14e %12.7f %12.7f %12.7f %12.7f %12.7f %12.7f %5.2f %5.2f %5.2f %5.2f %5.2f %5.2f %5.2f %5.2f %5.2f %5.2f %5.2f\n",\
           species2tag(atom.species,i+1), pbc(atom.x),pbc(atom.y),pbc(atom.z),\
           0.0, 0.0, 0.0,\
           0.0, 0.0,\
           0.0, 0.0, 0.0,\
           0.0, 0.0, 0.0,\
           0.0, 0.0, 0.0)
  end
end

def pbc(x)
  return x+1.0 if x <= 0.0
  return x-1.0 if x >  1.0
  return x
end

if ARGV[0] then
  read_POSCAR ARGV[0]
else
  read_POSCAR
end

out_pmd
