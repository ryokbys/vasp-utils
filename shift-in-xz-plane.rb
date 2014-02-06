#!/usr/bin/ruby
#
# USAGE:
#   $ ./shift-in-xz-plane.rb POSCAR.diamond.y111
# OUTPUT:
#   * POSCAR.###
#     ...about 50 POSCAR files will be created.
#

#.....add the directory where this file exists to the search path
$: << File.dirname(__FILE__)

require 'POSCAR.rb'

#.....parameters
NUM_DIVISION= 10

#=======================================================================
# Subroutines and functions
#=======================================================================
def pbc(x)
  return x+1.0 if x <= 0.0
  return x-1.0 if x >  1.0
  return x
end

#=======================================================================
# Main routines hereafter
#=======================================================================

if ARGV.length != 1  then
  p '[Error] wrong number of arguments.'
  p ' Usage:'
  p '   $ ./shift-in-xz-plane.rb POSCAR.diamond.y111'
  exit
end

fname= ARGV[0]

poscar= POSCAR.new
poscar.read(fname)
p poscar

#.....pick atoms to be shifted which are within 7/24 < y < 19/24
id_shift= []
i= 0
poscar.num_atoms.each do |ns|
  ns.times do
    posi= poscar.pos[i]
    id_shift.push(i) if (7.0/24 < posi[1] and posi[1] < 19.0/24)
    i += 1
  end
end

#p id_shift

#.....loop for shifting atom positions
dx= 1.0/3 /NUM_DIVISION
dz= 1.0/2 /NUM_DIVISION
sz= 0.0
num= 0
pos_orig= poscar.pos
while sz < 1.0/2 do
  sx= 1.0/3 *sz
  while sx < 1.0/3 -1.0/3*sz do 
    #.....initialize
    poscar.pos= pos_orig
    #.....shift
    id_shift.each do |i|
      (poscar.pos[i])[0] += sx
      (poscar.pos[i])[2] += sz
      (poscar.pos[i])[0] = pbc((poscar.pos[i])[0])
      (poscar.pos[i])[2] = pbc((poscar.pos[i])[2])
    end
    #.....write POSCAR
    p "writing POSCAR.%03d" % num
    poscar.write("POSCAR.%03d" % num)
    num += 1
    sx= sx +dx
  end
  sz= sz +dz
end
