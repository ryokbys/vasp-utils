#!/usr/bin/ruby
#
# Utilities related to OUTCAR
#

def get_magnetization(filename='OUTCAR')
  file=open(filename,"r")
  i=0
  while line=file.gets
    line.chomp!
    if line.include?("magnetization (x)") then
      #.....empty line
      file.gets
      #.....# of ion, s, p, d, tot
      file.gets
      #.....----
      file.gets
      magmoms=[]
      until (l=file.gets).include?("-----") do
        d= l.split
        magmoms << d[4]
      end
    end
  end
  file.close
  return magmoms
end

def get_charge(filename='OUTCAR')
  file=open(filename,"r")
  i=0
  while line=file.gets
    line.chomp!
    if line.include?("total charge") then
      #.....empty line
      file.gets
      #.....# of ion, s, p, d, tot
      file.gets
      #.....----
      file.gets
      chrgs=[]
      until (l=file.gets).include?("-----") do
        d= l.split
        chrgs << d[4]
      end
    end
  end
  file.close
  return chrgs
end

