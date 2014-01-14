#!/usr/bin/ruby
#
# Convert XDATCAR file to Akira-format files for creating a movie
#
# Usage:
#   $ ./XDATCAR2akr.rb
#
# Input: (these must be in the working directory)
#   - POSCAR (for the cell information)
#   - XDATCAR (atom configuration per each step)
#

#.....add the directory where this file exists to the search path
$: << File.dirname(__FILE__)

require 'MD_classes.rb'
require 'OUTCAR.rb'

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
  if $c7[0..0].downcase == 's' then
    #.....read another line
    $c8= file.gets
  end
  #.....9th--: atom positions
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

def out_Akira(akrname='akr000')
  akrfile=open(akrname,'w') do |line|
    line.printf(" %6d %3d %3d %3d\n",$system.natm,0,0,0)
    a1= $system.a1
    a2= $system.a2
    a3= $system.a3
    line.printf(" %12.7f %12.7f %12.7f\n", a1[0],a1[1],a1[2])
    line.printf(" %12.7f %12.7f %12.7f\n", a2[0],a2[1],a2[2])
    line.printf(" %12.7f %12.7f %12.7f\n", a3[0],a3[1],a3[2])
    i=0
    $system.natm.times do
      atom= $system.atoms[i]
      line.printf("%3d %12.7f %12.7f %12.7f \n",
                  atom.species, atom.x,atom.y,atom.z)
      i+=1
    end
  end
end

def pbc(x)
  x = x + 1.0 if x < 0.0
  x = x - 1.0 if x >= 1.0
  return x
end

#============================== start main program here
read_POSCAR

#.....Angstrom to Bohr radius
(0..2).each do |i|
  $system.a1[i] *= AA2BOHR
  $system.a2[i] *= AA2BOHR
  $system.a3[i] *= AA2BOHR
end


infname='./XDATCAR'
if ARGV[0] then
  infname=ARGV[0]
end

file=open(infname,'r')
#.....check num of atoms
natm=file.gets.split[0].to_i
if natm != $system.natm then
  print " [Error] natm in XDATCAR differs from natm in POSCAR !!!\n"
  exit 1
end
#.....skip some lines
cskip=file.gets
cskip=file.gets
cskip=file.gets
cskip=file.gets
cskip=file.gets

#.....output akr000 from POSCAR data
out_Akira 'akr000'

pos=[]
ifile=0
while !file.eof
  ifile= ifile +1
  $system.natm.times do |ia|
    pos=file.gets.split
    pos[0]= pbc(pos[0].to_f)
    pos[1]= pbc(pos[1].to_f)
    pos[2]= pbc(pos[2].to_f)
    $system.atoms[ia].x=pos[0]
    $system.atoms[ia].y=pos[1]
    $system.atoms[ia].z=pos[2]
  end
  out_Akira "akr%03d"%[ifile]
  cskip=file.gets
end
file.close
