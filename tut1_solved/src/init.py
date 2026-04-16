from netpyne import sim
from netParams import netParams  
from cfg import simConfig            

# Create network and run simulation
sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)

if sim.rank == 0:  # only plot on master node
    num_spikes = len(sim.allSimData.get('spkt', []))
    num_cells = len(sim.net.cells)
    duration_s = sim.cfg.duration / 1e3 if sim.cfg.duration else 0.0
    mean_rate_hz = num_spikes / (num_cells * duration_s) if num_cells and duration_s else 0.0

    sim.send({
        'simLabel': sim.cfg.simLabel,
        'numSpikes': num_spikes,
        'numCells': num_cells,
        'meanRateHz': mean_rate_hz,
    })
