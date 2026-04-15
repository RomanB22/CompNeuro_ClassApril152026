"""
cfg.py  -  Simulation configuration for the Brunel-Hakim (1999) model
           implemented in NetPyNE / NEURON.

This file owns:
  - simulation timing and numerics
  - LIF neuron parameters (forwarded to lif.mod via netParams.py)
  - network-level scalars (N, C, J, delay)
  - recording, output, and analysis settings

netParams.py reads these values to build the network; it does NOT
hard-code any biological numbers.

Reference: Brunel N & Hakim V (1999) Neural Comput 11:1621-1671.
"""
from netpyne import specs

cfg = specs.SimConfig()

# ─── Simulation ───────────────────────────────────────────────────────────────
cfg.duration     = 200.0    # ms   (original paper used 100 ms; extend for stats)
cfg.dt           = 0.1       # ms   fixed time step
cfg.verbose      = False
cfg.printRunTime = 0.5       # ms of sim time between progress prints
cfg.seeds        = {'conn': 42, 'stim': 42, 'loc': 42}
cfg.hParams      = {'v_init': 10.0}   # initial section voltage [mV] (= Vr)

# ─── LIF Neuron Parameters ────────────────────────────────────────────────────
cfg.tau          = 20.0      # ms   membrane time constant
cfg.theta        = 20.0      # mV   spike threshold
cfg.Vr           = 10.0      # mV   reset potential
cfg.taurefr      = 2.0       # ms   absolute refractory period
cfg.muext        = 80.0      # mV   mean external drive (encodes mu_ext from paper)
cfg.sigmaext     = 7       # mV   amplitude of Gaussian noise drive (sigma_ext)

# ─── Network Parameters ───────────────────────────────────────────────────────
cfg.scale        = 0.2
cfg.N            = int(cfg.scale*5000)      # total number of neurons
cfg.C            = int(cfg.scale*1000)      # recurrent in-degree (connections received per neuron)
cfg.J            = 1.5       # mV   synaptic weight magnitude; applied as -J (inhibitory)
cfg.delay        = 2.0       # ms   synaptic transmission delay (delta in paper)

# ─── Best params combinations ────────────────────────────────────────────────────────────────
# cfg.sigmaext, cfg.J, cfg.muext = [1.2, 0.1, 25.0], [5, 0.5, 80.]
# ─── Recording ────────────────────────────────────────────────────────────────
# Record the LIF internal voltage V from a handful of example cells.
# NetPyNE variable format for point-process RANGE vars: '<MOD>_<VAR>'
cfg.recordTraces = {
    'V_lif': {'sec': 'soma', 'pointp': 'LIF', 'var': 'V'}   # record LIF internal voltage
}
cfg.recordCells  = [0, 1, 2]    # cell indices to record traces from
cfg.recordStep   = 0.1           # ms   trace sampling interval

# ─── Output ───────────────────────────────────────────────────────────────────
cfg.filename      = 'output/brunel_hakim'
cfg.savePickle    = False
cfg.saveJson      = True
cfg.saveCellSecs  = False   # skip full section data → much smaller JSON
cfg.saveCellConns = False   # skip 5M connection records → avoids ~1 GB output

# ─── Analysis ─────────────────────────────────────────────────────────────────
cfg.transient = 50.0      # ms   time to exclude from analysis (to skip transient dynamics)
cfg.timeRange = [cfg.transient, 150.]   # ms   time range to analyze (after transient)
cfg.analysis['plotRaster'] = {
    'timeRange': cfg.timeRange,
    'saveFig':   True,
    'showFig':   False,
}
cfg.analysis['plotTraces'] = {
    'include':   [0, 1, 2],
    'timeRange': cfg.timeRange,
    'saveFig':   True,
    'showFig':   False,
}
cfg.analysis['plotSpikeStats'] = {
    'stats':     ['rate'],
    'timeRange': cfg.timeRange,
    'saveFig':   True,
    'showFig':   False,
}
cfg.analysis['plotSpikeHist'] = {
    'timeRange': cfg.timeRange,   
    'binSize':   0.1,      # ms   bin size
    'saveFig':   True,
    'showFig':   False,
}

cfg.analysis['plotSpikeFreq'] = {
    'timeRange': cfg.timeRange,
    'binSize':   0.1,      # ms   bin size
    'saveFig':   True,
    'showFig':   False,
}