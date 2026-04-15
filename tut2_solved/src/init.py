from netpyne import sim
from netParams import netParams  
from cfg import simConfig            

# Create network and run simulation
sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)
