#!/usr/bin/ruby
#encoding: utf-8
#-----------------------------------------------------------------------
# Utilities related to POTCAR
#-----------------------------------------------------------------------

def read_POTCAR(filename='POTCAR')
  file=open(filename,'r')
  #.....initialize
  species=[]
  valence=[]
  encut=[]
  #.....search lines of ' PAW_PBE....??Jan20??'
  isp= 0
  sp= /^\sPAW_PBE\s*\s[12]*/
  enmax= /^\s+ENMAX\s+.*/
  while line = file.gets
    line.chomp!
    if sp =~ line then
      isp=isp +1
      data= line.split
      species[isp-1]= data[1] # speciess name
      #.....read next line
      valence[isp-1]= file.gets.chomp.to_f
    end
    if enmax =~ line then
      data= line.split
      encut[isp-1]= data[2].to_f
    end
  end
  #.....returning data
  potcar= Hash::new
  potcar['num_species']= isp
  potcar['species']= species
  potcar['valence']= valence
  potcar['encut']= encut
  return potcar
end

if ARGV[0] then
  potcar= read_POTCAR ARGV[0]
else
  potcar= read_POTCAR
end

