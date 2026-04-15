"""
netParams.py  -  Network architecture for the Brunel-Hakim (1999) model.

Network summary
---------------
* N = 5000 identical LIF neurons forming a single all-inhibitory population.
* External drive is encoded directly inside each LIF (muext bias + sigmaext noise).
* Recurrent connectivity: each neuron receives C = 1000 inhibitory inputs drawn
  randomly with probability p = C / N = 0.2 (sparse, fixed-in-degree approximation).
* Synaptic interaction: instantaneous voltage shift of -J = -0.1 mV after a
  fixed delay delta = 2 ms (delta/kick synapse, no kinetics needed).

All numerical values come from cfg.py to keep this file purely structural.

Reference: Brunel N & Hakim V (1999) Neural Comput 11:1621-1671.
"""
from netpyne import specs
from cfg import cfg

netParams = specs.NetParams()

# ─── Cell Type: LIF Point Neuron ──────────────────────────────────────────────
# A minimal passive soma section is required by NEURON/NetPyNE topology.
# All electrical dynamics (membrane integration, noise, threshold, reset,
# refractoriness) live inside the LIF POINT_PROCESS defined in mod/lif.mod.
netParams.cellParams['LIF_cell'] = {
    'secs': {
        'soma': {
            'geom': {'L': 10, 'diam': 10},   # placeholder geometry; not used electrically
            'pointps': {
                'LIF': {
                    'mod':      'LIF',
                    'tau':      cfg.tau,
                    'theta':    cfg.theta,
                    'Vr':       cfg.Vr,
                    'taurefr':  cfg.taurefr,
                    'muext':    cfg.muext,
                    'sigmaext': cfg.sigmaext,
                    'vref':     'V',   # tells NetPyNE this pointp holds the cell voltage
                                       # (artificial cell pattern); connections route here
                }
            }
        }
    }
}

# ─── Population ───────────────────────────────────────────────────────────────
# Single homogeneous population of N LIF neurons.
netParams.popParams['BHpop'] = {
    'cellType': 'LIF_cell',
    'numCells': cfg.N,
}

# ─── Recurrent Inhibitory Connections ─────────────────────────────────────────
# Connection probability p = C / N yields an expected in-degree of C per neuron.
# Weights are negative (inhibitory); spikes arrive after a fixed delay.
# 'synMech': 'LIF' routes incoming spikes to the LIF point process NET_RECEIVE,
#            which directly shifts V by weight (no additional synapse mechanism
#            is needed for this delta/kick model).
netParams.connParams['BH->BH'] = {
    'preConds':    {'pop': 'BHpop'},
    'postConds':   {'pop': 'BHpop'},
    'probability':  float(cfg.C) / cfg.N,   # = 0.2
    'weight':      -cfg.J,                   # mV  (negative = inhibitory)
    'delay':        cfg.delay,               # ms
    'synMech':     'LIF',                    # target: LIF point process NET_RECEIVE
    'sec':         'soma',
    'loc':          0.5,
}
