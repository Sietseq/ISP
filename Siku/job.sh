#!/bin/bash

#SBATCH --time=40:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=8
#SBATCH --account=an-tr043
#SBATCH --output=$1.out

# Creates python virtual environment pip libraries.s
module load python/3.10
module list 
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index --upgrade pip
pip install --no-index patool 

# Run script.
python extract.py $1

