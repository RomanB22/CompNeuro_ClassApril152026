"""
init.py  -  Entry point for the Brunel-Hakim (1999) NetPyNE / NEURON model.

Usage
-----
    # Activate the conda environment (DISPLAY should be unset for headless runs)
    conda activate CompNeuroCourse
    unset DISPLAY

    # From inside the BrunelHakim/ directory:
    python init.py

The script will compile mod/lif.mod automatically on first run (requires
nrnivmodl on PATH, which is provided by the NEURON package in the conda env).
Figures and data are saved to output/.
"""
import os
import sys
import subprocess

# ─── Compile NEURON mod files ─────────────────────────────────────────────────
# nrnivmodl writes the compiled library to x86_64/ (or arm64/ on Apple Silicon).
_arch_dirs = ['x86_64', 'arm64', 'i686']
_compiled  = any(
    os.path.isfile(os.path.join(d, 'special'))
    for d in _arch_dirs
    if os.path.isdir(d)
)
if not _compiled:
    print('[init] Compiling mod files with nrnivmodl ...')
    result = subprocess.run(
        ['nrnivmodl', 'mod'],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit(f'[init] ERROR: nrnivmodl failed.\n{result.stderr}')
    print('[init] Compilation successful.')

# ─── Ensure output directory exists ──────────────────────────────────────────
os.makedirs('output', exist_ok=True)

# ─── NetPyNE simulation ───────────────────────────────────────────────────────
# Imports must come after mod compilation so NEURON can load the mechanisms.
from netpyne import sim       
from netParams import netParams  
from cfg import cfg              

sim.createSimulateAnalyze(netParams=netParams, simConfig=cfg)
