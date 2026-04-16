from netpyne.batchtools.search import search, grid

# -------------------------------------------------------------------------
# Batch parameters – grid search over simConfig.seeds sub-keys
# -------------------------------------------------------------------------
params = {
    'seeds.conn': [1, 2, 3],
    'seeds.stim': [1, 2, 3],
    'seeds.loc':  [1, 2, 3],
}

# -------------------------------------------------------------------------
# Run the grid search (27 combinations: 3 x 3 x 3)
# -------------------------------------------------------------------------
run_configDownstate={
        'env': 'conda activate CompNeuroCourse',
        'script': 'python -u src/init.py',
        'cores': 1,
        'mem': '8G',
        'realtime': '00:30:00'
    }

search(
    job_type='sh',      # change to 'suny' for cluster
    comm_type = 'socket', # 'socket', 'sfs', None
    params=params,
    run_config={
        'command': 'python -u src/init.py',
    },
    label='gridSearch_seeds',
    output_path='./batch_results',
    checkpoint_path='./batch_checkpoints',
)
