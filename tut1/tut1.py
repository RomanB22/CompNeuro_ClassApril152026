import HHTut
from netpyne import sim
sim.createSimulateAnalyze(netParams = HHTut.netParams, simConfig = HHTut.simConfig)

from pprint import pprint
pprint(sim.specs.simConfig.__dict__)
pprint(HHTut.simConfig.__dict__)
pprint(sim.specs.netParams.__dict__)
pprint(HHTut.netParams.__dict__)
pprint(sim.__dict__)

import json

def save_json(obj, filename):
    with open(filename, "w") as f:
        json.dump(obj, f, indent=2, default=str)

save_json(sim.specs.simConfig.__dict__, "sim_specs_simConfig.json")
save_json(HHTut.simConfig.__dict__, "HHTut_simConfig.json")
save_json(sim.specs.netParams.__dict__, "sim_specs_netParams.json")
save_json(HHTut.netParams.__dict__, "HHTut_netParams.json")
save_json(sim.__dict__, "sim_dict.json")