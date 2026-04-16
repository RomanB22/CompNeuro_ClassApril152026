from netpyne.batchtools.search import search

params = {'nmda.PYR->BC' : [1e-3, 1.8e-3],
          #'nmda.PYR->OLM': [0.4e-3, 1.0e-3],
          #'nmda.PYR->PYR': [0.001e-3, 0.007e-3],
          'ampa.PYR->BC' : [0.2e-3, 0.5e-3],
          #'ampa.PYR->OLM': [0.2e-3, 0.5e-3],
          #'ampa.PYR->PYR': [0.01e-3, 0.03e-3],
          #'gaba.BC->BC'  : [1e-3, 7e-3],
          'gaba.BC->PYR' : [0.4e-3, 1.0e-3],
          #'gaba.OLM->PYR': [40e-3, 100e-3],
          }

# use batch_shell_config if running directly on the machine
run_config={
    'command': 'python -u init.py',
}

search(job_type = 'sh', # 'sh', and ssh based options
       comm_type = 'socket', # 'socket', 'sfs', None
       label = 'optuna',
       params = params,
       output_path = './batch',
       checkpoint_path = './checkpoint',
       advanced_logging = True,
       run_config = run_config,
       num_samples = 27,
       metric = 'loss',
       mode = 'min',
       algorithm = 'optuna',
       max_concurrent = 3)
