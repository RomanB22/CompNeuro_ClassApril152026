#!/bin/bash
#SBATCH --job-name=tut1_solved_mpi
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=8G
#SBATCH --time=00:30:00
#SBATCH --output=slurm-%x-%j.out
#SBATCH --error=slurm-%x-%j.err

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
MODEL_DIR="$PROJECT_DIR/tut1_solved"

cd "$PROJECT_DIR"
source ~/.bashrc
conda activate CompNeuroCourse
# For the Downstate cluster
export LD_LIBRARY_PATH=~/miniconda3/envs/CompNeuroCourse/lib
export UCX_TLS=tcp,self # To prevent error with MPI memory allocation

cd "$MODEL_DIR"
export PYTHONPATH="$MODEL_DIR${PYTHONPATH:+:$PYTHONPATH}"
# # Compile mechanisms once before launching MPI so ranks do not race on nrnivmodl.
# if [ ! -x x86_64/special ] && [ ! -x arm64/special ] && [ ! -x i686/special ]; then
#     nrnivmodl mod
# fi

mpiexec -n "${SLURM_NTASKS:-4}" nrniv -python -mpi src/init.py
