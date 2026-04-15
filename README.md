# CompNeuro_ClassApril152026

Simple `NetPyNE` and pure `NEURON` implementations of the Brian2 Brunel-Hakim 1999 inhibitory network:
https://brian2.readthedocs.io/en/stable/examples/frompapers.Brunel_Hakim_1999.html

The layout follows the usual NetPyNE example split:

- `netpyne_model/init.py`: setup and run
- `netpyne_model/cfg.py`: simulation configuration
- `netpyne_model/netParams.py`: network parameters
- `netpyne_model_precomputed/init.py`: same model, but with one cached edge list loaded into NetPyNE
- `netpyne_model_precomputed/cfg.py`: simulation configuration for the precomputed-connectivity NetPyNE example
- `netpyne_model_precomputed/netParams.py`: explicit connection list version of the network
- `cells/brunel_hakim_cell.py`: imported cell template
- `mod/BrunelHakimIF.mod`: shared custom point-process dynamics
- `neuron_model/init.py`: pure NEURON setup and run
- `neuron_model/config.py`: pure NEURON simulation configuration
- `neuron_model/network.py`: pure NEURON network build
- `neuron_model_precomputed/init.py`: pure NEURON run using the same cached edge list as NetPyNE
- `neuron_model_precomputed/config.py`: pure NEURON simulation configuration for the precomputed example
- `neuron_model_precomputed/network.py`: pure NEURON network build from the shared edge list
- `shared/connectivity.py`: generation and caching of the shared edge list

The default configuration uses `netScale = 0.1` so it stays easy to run locally. Set `netScale = 1.0`
in `netpyne_model/cfg.py` and `neuron_model/config.py` to match the Brian2 example size exactly
(`N = 5000`, `C = 1000`, `p = 0.2`).

## Run

Compile the mechanism first:

```bash
env -u DISPLAY conda run -n CompNeuroCourse nrnivmodl mod
```

Run the NetPyNE version:

```bash
env -u DISPLAY MPLCONFIGDIR=/tmp/mplconfig conda run -n CompNeuroCourse python netpyne_model/init.py
```

Run the pure NEURON version:

```bash
env -u DISPLAY MPLCONFIGDIR=/tmp/mplconfig conda run -n CompNeuroCourse python neuron_model/init.py
```

Run the NetPyNE version with precomputed shared connectivity:

```bash
env -u DISPLAY MPLCONFIGDIR=/tmp/mplconfig conda run -n CompNeuroCourse python netpyne_model_precomputed/init.py
```

Run the pure NEURON version with the same precomputed shared connectivity:

```bash
env -u DISPLAY MPLCONFIGDIR=/tmp/mplconfig conda run -n CompNeuroCourse python neuron_model_precomputed/init.py
```

The original `netpyne_model/` and `neuron_model/` examples intentionally generate connectivity independently,
so their exact edge sets differ slightly. The `*_precomputed/` examples instead read the same cached edge list
from `data/connectivity/`, which makes the network graph identical in both frameworks.

All runs save a raster plus population-rate figure and a small `summary.json` file under `data/`.
