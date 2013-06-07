#!/usr/bin/ruby
#
# Split CHG file to total (up+down), magnetic (up-down) densities
#

def read_CHG(filename=`CHG`)
  file= open(filename)
  $comment= file.gets
  $afac= file.gets
  $a1=[]
  $a2=[]
  $a3=[]
  #.....a1
  data=file.gets.split
  data.each_with_index do |d,i|
    $a1[i]= d.to_f
  end
  #.....a2
  data=file.gets.split
  i=0
  data.each_with_index do |d,i|
    $a2[i]= d.to_f
  end
  #.....a3
  data=file.gets.split
  data.each_with_index do |d,i|
    $a3[i]= d.to_f
  end
  #.....number of atoms
  $natms=[]
  data=file.gets.split
  data.each_with_index do |d,i|
    $natms[i]= d.to_i
  end
  #....."Direct"
  $c7= file.gets
  #.....atom positions
  $pos=[]
  ib= 0
  $natms.each_with_index do |natm,is|
    i= ib
    natm.times do
      data=file.gets.split
      $pos[i+0]= data[0].to_f
      $pos[i+1]= data[1].to_f
      $pos[i+2]= data[2].to_f
      i += 3
    end
    ib += natm*3
  end
  #.....blank line
  data=file.gets
  #.....NGX,NGY,NGZ
  data=file.gets.split
  $ngx= data[0].to_i
  $ngy= data[1].to_i
  $ngz= data[2].to_i
  ng= $ngx *$ngy *$ngz
  #.....volumetric data
  ndline= ng/10
  ngmod= ng%10
  if ngmod != 0 then
    puts " [Error] ngmod != 0"
    puts " This program is not applicable to the case ngmod != 0..."
    exit(1)
  end
  #.....total
  $dtot=[]
  ndline.times do
    data=file.gets.split
    data.each do |d|
      $dtot << d.to_f
    end
  end
  #.....NGX,NGY,NGZ again
  data=file.gets.split
  #.....deviation (magnetic)
  $dmag=[]
  ndline.times do
    data=file.gets.split
    data.each do |d|
      $dmag << d.to_f
    end
  end
  file.close
end


def write_CHG(filename='CHG.out',data=Array.new)
  if data.size != $ngx*$ngy*$ngz then
    puts " [Error] data.size != $ngx*$ngy*$ngz !!!"
    puts "data.size= ",data.size
    puts "$ngx*$ngy*$ngz= ",$ngx*$ngy*$ngz
    exit(1)
  end
  file=open(filename,"w")
  file.puts $comment
  file.puts $afac
  file.printf(" %12.7f %12.7f %12.7f\n",$a1[0],$a1[1],$a1[2])
  file.printf(" %12.7f %12.7f %12.7f\n",$a2[0],$a2[1],$a2[2])
  file.printf(" %12.7f %12.7f %12.7f\n",$a3[0],$a3[1],$a3[2])
  $natms.each do |natm|
    file.printf(" %5d",natm)
  end
  file.printf(" \n")
  file.puts $c7
  i=0
  ($pos.size/3).times do
    file.printf(" %12.7f %12.7f %12.7f\n",$pos[i+0],$pos[i+1],$pos[i+2])
    i+=3
  end
  #.....blank line
  file.puts " "
  #.....number of volumetric data
  file.printf(" %5d %5d %5d\n",$ngx,$ngy,$ngz)
  #.....volumetric data
  data.each_with_index do |d,i|
    file.printf(" %13.6e",d)
    file.printf("\n") if i%10 == 9
  end
  file.close
end

CHG_FNAME= ARGV[0]
read_CHG CHG_FNAME
write_CHG "CHG.tot",$dtot
write_CHG "CHG.mag",$dmag

