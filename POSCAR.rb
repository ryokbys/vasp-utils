#!/usr/bin/ruby
#
# POSCAR related functions
#
#

#.....add the directory where this file exists to the search path
$: << File.dirname(__FILE__)

class POSCAR
  attr_accessor :c1,:afac,:a1,:a2,:a3,:num_atoms,:c7,:c8,:pos,:flags

  #AA2BOHR= 1.88972616356
  AA2BOHR= 1.0/0.5291772

  def initialize()
    @a1= []
    @a2= []
    @a3= []
    @num_atoms= []
    @pos= []
    @flags= []
  end

  def read(filename="./POSCAR")
    file= open(filename)
    #.....1st line: comment
    @c1=file.gets
    #.....2nd line: multiply factor
    @afac= file.gets.to_f
    #.....3rd-5th lines: lattice vectors
    data= file.gets.split
    3.times do |i|
      @a1[i]= data[i].to_f
    end
    data= file.gets.split
    3.times do |i|
      @a2[i]= data[i].to_f
    end
    data= file.gets.split
    3.times do |i|
      @a3[i]= data[i].to_f
    end
    #.....6th line: num of atoms
    i=0
    (file.gets.split).each do |n|
      @num_atoms[i]= n.to_i
      i += 1
    end
    #.....7th line: comment
    @c7= file.gets
    if @c7[0..0].downcase == 's' then
      #.....read another line
      @c8= file.gets
    end
    #.....8th--: atom positions
    sid=0
    @num_atoms.each do |n|
      (0..n-1).each do |j|
        data= file.gets.split
        @pos.push([data[0].to_f,data[1].to_f,data[2].to_f])
        if data.length > 3 then
          if data.length == 6 then
            @flags.push([data[3],data[4],data[5]])
          elsif data.length == 4 then
            @flags.push([data[3],data[4],data[4]])
          end
        else
          @flags.push(["T","T","T"])
        end
      end
    end
    file.close
  end

  def write(filename='POSCAR')
    file= open(filename,'w')
    file.write(@c1)
    file.write(" %10.5f\n" % @afac)
    file.write(" %12.7f %12.7f %12.7f\n" % @a1)
    file.write(" %12.7f %12.7f %12.7f\n" % @a2)
    file.write(" %12.7f %12.7f %12.7f\n" % @a3)
    @num_atoms.each do |n|
      file.write(" %d " % n)
    end
    file.write("\n")
    file.write(@c7)
    file.write(@c8) if @c8
    @pos.length.times do |i|
      file.write(" %12.7f %12.7f %12.7f" % @pos[i])
      file.write(" %s %s %s\n" % @flags[i])
    end
    file.close
  end

end

# poscar= POSCAR.new
# poscar.read
# poscar.write('new_POSCAR')
