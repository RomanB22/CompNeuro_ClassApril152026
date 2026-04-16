from netpyne import specs

# Simulation options
simConfig = specs.SimConfig()       # object of class SimConfig to store simulation configuration

###############################################################################
# SIMULATION PARAMETERS
###############################################################################

# Simulation parameters
simConfig.duration = 1*1e3 # Duration of the simulation, in ms
simConfig.dt = 0.025 # Internal integration timestep to use
simConfig.seeds = {'conn': 1, 'stim': 1, 'loc': 1} # Seeds for randomizers (connectivity, input stimulation and cell locations)
simConfig.verbose = False  # show detailed messages
simConfig.vinit = -71
simConfig.hParams = {'v_init': simConfig.vinit}

# Recording
simConfig.recordCells = []  # which cells to record from
simConfig.recordTraces = {'Vsoma': {'sec': 'soma','loc': 0.5,'var': 'v'}}
simConfig.recordStim = True  # record spikes of cell stims
simConfig.recordStep = 0.1 # Step size in ms to save data (eg. V traces, LFP, etc)

# Saving
simConfig.filename = 'HHTut'  # Set file output name
simConfig.savePickle = False # Whether or not to write spikes etc. to a .mat file
simConfig.saveJson = True

# Analysis and plotting
simConfig.analysis['plotRaster'] = {'saveData': 'raster_data.json', 'saveFig': True, 'showFig': True} # Plot raster
simConfig.analysis['plotTraces'] = {'include': [2], 'saveFig': True, 'showFig': True} # Plot cell traces
simConfig.analysis['plot2Dnet'] = {'saveFig': True, 'showFig': True} # Plot 2D cells and connections


simConfig.validateNetParams=True