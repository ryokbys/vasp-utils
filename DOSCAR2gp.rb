#!/usr/bin/ruby
#
# extracts DOS info from DOSCAR file
#

def read_DOSCAR(filename='DOSCAR')
  file=open(filename,"r")
  #.....1st line
  l1= file.gets
  #.....2nd line
  l2= file.gets
  #.....3rd line
  l3= file.gets
  #.....4th line
  l4= file.gets
  #.....5th line
  l5= file.gets
  #.....6th line
  l6= file.gets
  d6= l6.split
  e_max= d6[0].to_f
  e_min= d6[1].to_f
  num_line= d6[2].to_i
  fermi= d6[3].to_f

  #.....total dos
  tdos=[]
  spin= 0
  num_line.times do |i|
    tdos.push(file.gets.split)
    #.....check spin-polarization
    if i==0 then
      #.....set unpolarized
      spin=1
      if tdos[i].length > 3 then
        #.....set polarized
        spin=2
      end
    end
  end

  #.....L decomposed dos
  if file.gets then
    ldos=[]
    num_line.times do |i|
      ldos.push(file.gets.split)
    end
  end

  file.close

  #.....doscar data
  doscar= Hash::new
  doscar['fermi']= fermi
  doscar['e_max']= e_max
  doscar['e_min']= e_min
  doscar['spin']= spin
  doscar['tdos']= tdos
  doscar['ldos']= ldos
  return doscar
end

doscar= read_DOSCAR(ARGV[0])
tdos= doscar['tdos']
ldos= doscar['ldos']
spin= doscar['spin']
fermi= doscar['fermi']
tdos.length.times do |i|
  dtdos= tdos[i]
  data= []
  str= ''
  if ldos then # with l-decomposed dos
    dldos= ldos[i]
    if spin==1 then
      data.push(dtdos[0].to_f-fermi)
      str += " %10.3f"
      data.push(dtdos[1].to_f)
      str += " %10.5f"
      (1..(dldos.length-1)).each do |j|
        data.push(dldos[j].to_f)
        str += " %10.5f"
      end
      puts str % data
    elsif spin==2 then
      data.push(dtdos[0].to_f-fermi)
      str += " %10.3f"
      data.push(dtdos[1].to_f)
      str += " %10.5f"
      data.push(dtdos[2].to_f)
      str += " %10.5f"
      (1..(dldos.length-1)).each do |j|
        data.push(dldos[j].to_f)
        str += " %10.5f"
      end
      puts str % data
    end

  else # only total dos
    if spin==1 then
      puts " %10.3f %10.5f" % [dtdos[0],dtdos[1]]
    elsif spin==2 then
      puts " %10.3f %10.5f %10.5f" % [dtdos[0],dtdos[1],dtdos[2]]
    end
  end
end
