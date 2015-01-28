# What's this package
This package includes some utilities that help us process outputs 
obtained through VASP calculations.

# Who made this?
* Ryo KOBAYASHI
* Assistant Professor in the department of mechanical engineering, Nagoya Institute of Technology. (2014-01-07)

------

# Usage

## XDATCAR2.py
It requires that INCAR, POSCAR, and XDATCAR files exist in the working directory.
```
$ python XDATCAR2.py -s POSCAR
```
will create POSCAR???? files of atom positions written in XDATCAR.
Cell vectors are taken from POSCAR and kept constant for every POSCAR???? files.


# Etot-vs-size.py
This will calculate several different size of cells and show a graph of cohesive energy versus cell volume.
```
$ python Etot-vs-size.py 5.3 5.5
```
The arguments are the min and max of lattice constant written at the 2nd line of POSCAR.

Options:
* `-n`: Number of points between min and max to be calculated.
* `--no-graph`: Do not show graph using matplotlib. In case of slow connection to a remote host...


