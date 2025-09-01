#!/bin/bash
#SBATCH --job-name=velo_sweep
#SBATCH --output=logs/array_%A_%a.out
#SBATCH --error=logs/array_%A_%a.err
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
# EDIT THIS RANGE to match number of rows in params.csv (0..N-1)
#SBATCH --array=0-4

set -euo pipefail

module purge || true
# If Apptainer is available via module:
# module load apptainer

mkdir -p logs results

ROW_IDX=${SLURM_ARRAY_TASK_ID}
BASE_SEED=0

# Bare-metal (no container):
# python run_one.py --params params.csv --row-index ${ROW_IDX} --out-dir results --base-seed ${BASE_SEED}

# With Apptainer/Singularity (recommended on HPC):
apptainer exec --bind "$PWD:$PWD" containers/velo.sif \
  python 4_cluster_slurm/run_one.py --params 4_cluster_slurm/params.csv \
  --row-index ${ROW_IDX} --out-dir 4_cluster_slurm/results --base-seed ${BASE_SEED}
