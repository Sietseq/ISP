#!/bin/bash
sbatch <<EOT
#!/bin/bash

#SBATCH --time=40:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=1000M
#SBATCH --account=an-tr043
#SBATCH --output=./out/$1.out

# Creates python virtual environment pip libraries.s
module load python/3.10
pip install --no-index --upgrade pip
pip install --no-index patool

# Run script.
python extract.py $1
exit 0
EOT
