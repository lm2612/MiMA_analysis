#!/bin/bash

#SBATCH --job-name=plot_T62   # job name
#SBATCH --partition=serc     # partition
#SBATCH --time=2:00:00       # walltime
#SBATCH --ntasks=1           # number of processor cores (i.e. tasks)
#SBATCH --nodes=1            # number of nodes
#SBATCH --mem=64G            # large mem needed
#SBATCH --output=/scratch/users/lauraman/MiMA/jobs/PlotT62_%j.out
#SBATCH --error=/scratch/users/lauraman/MiMA/jobs/PlotT62_%j.err

## Save Plots for high res simulation (large mem required)
. /home/users/lauraman/miniconda3/etc/profile.d/conda.sh
export PATH="/home/users/lauraman/miniconda3/bin:$PATH"
conda activate plot_env

cd /home/users/lauraman/MiMA_analysis/

python -m Scripts.SavePlots_T62
