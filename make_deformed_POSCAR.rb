#!/usr/bin/ruby
#encoding: utf-8
#-----------------------------------------------------------------------
# Make deformed POSCAR files from the non-deformed POSCAR file.
# Deformation is performed by multiplying deformation matrix to h-mat.
#-----------------------------------------------------------------------
# Usage:
#   $ PATH/make_deformed_POSCAR.rb POSCAR POSCAR.new

#.....add the directory where this file exists to the search path
$: << File.dirname(__FILE__)

require 'POSCAR.rb'

INITIAL_NUMBER= 0
DEV= [-0.05, 0.0, 0.05]

poscar= POSCAR.new
if ARGV[0] then
  poscar.read(ARGV[0])
else
  poscar.read
end

# original a vectors
a1o= poscar.a1
a2o= poscar.a2
a3o= poscar.a3
a1= [0.0, 0.0, 0.0]
a2= [0.0, 0.0, 0.0]
a3= [0.0, 0.0, 0.0]
inc= INITIAL_NUMBER
DEV.each do |e11|
  DEV.each do |e22e33|
    DEV.each do |g12|
      DEV.each do |g23g31|
        a1[0]= (1.0+e11)*a1o[0] +g12         *a1o[1] +g23g31      *a1o[2]
        a1[1]= g12      *a1o[0] +(1.0+e22e33)*a1o[1] +g23g31      *a1o[2]
        a1[2]= g23g31   *a1o[0] +g23g31      *a1o[1] +(1.0+e22e33)*a1o[2]
        a2[0]= (1.0+e11)*a2o[0] +g12         *a2o[1] +g23g31      *a2o[2]
        a2[1]= g12      *a2o[0] +(1.0+e22e33)*a2o[1] +g23g31      *a2o[2]
        a2[2]= g23g31   *a2o[0] +g23g31      *a2o[1] +(1.0+e22e33)*a2o[2]
        a3[0]= (1.0+e11)*a3o[0] +g12         *a3o[1] +g23g31      *a3o[2]
        a3[1]= g12      *a3o[0] +(1.0+e22e33)*a3o[1] +g23g31      *a3o[2]
        a3[2]= g23g31   *a3o[0] +g23g31      *a3o[1] +(1.0+e22e33)*a3o[2]
        poscar.a1= a1
        poscar.a2= a2
        poscar.a3= a3
        inc=inc +1
        poscar.write("POSCAR.%03d" % inc)
      end
    end
  end
end

