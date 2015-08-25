#!/bin/bash
#PBS -N calc-Etot-vs-size
#PBS -o out
#PBS -q batch
#PBS -j oe
#PBS -l nodes=2:ppn=4
#-----------------------------------------------------------------------
# Usage:
#   $ qsub run_vasp.sh
#-----------------------------------------------------------------------

export LANG=en_US
cd $PBS_O_WORKDIR
NPROCS=`wc -l < $PBS_NODEFILE`
cat $PBS_NODEFILE
echo 'NPROCS=' $NPROCS
#MPIRUN=/usr/local/openmpi-1.4.2-intel64-v11.1.073/bin/mpirun
MPIRUN=/opt/intel/impi/4.0.0.028/intel64/bin/mpirun
#vaspexec=/opt/vasp/bin/vasp
vaspexec=$HOME/bin/vasp
jobid=$PBS_JOBID

#rm OUTCAR
#rm CHG* CONTCAR WAVECAR
#$MPIRUN -recvtimeout 100 -np $NPROCS $vaspexec
#$MPIRUN -recvtimeout 100 -machinefile $PBS_NODEFILE -np $NPROCS $vaspexec
#mpirun -machinefile $PBS_NODEFILE -np $NPROCS $vaspexec
python ~/src/vasp-utils/Etot-vs-size.py --cmd="$MPIRUN -recvtimeout 100 -np $NPROCS $vaspexec" 5.0


