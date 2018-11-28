#!/bin/sh

# properties = {"type": "single", "rule": "all", "local": true, "input": ["s3://hboi-jobs/Pbceti_genome/01-trimmed/LP2W16W_1k_R1_001_val_1.fq.gz", "s3://hboi-jobs/Pbceti_genome/01-trimmed/LP2W16W_1k_R2_001_val_2.fq.gz"], "output": [], "wildcards": {}, "params": {}, "log": [], "threads": 1, "resources": {}, "jobid": 0, "cluster": {}}

\

python \

-m snakemake all --snakefile simple_trim_batch.snake \

--force -j --keep-target-files --keep-remote \

--wait-for-files  --latency-wait 5 \

 --attempt 1 --force-use-threads \

--wrapper-prefix https://bitbucket.org/snakemake/snakemake-wrappers/raw/ \

   --nocolor \

--notemp --no-hooks --nolock --mode 2  --use-conda  --allowed-rules all  && exit 0 || exit 1



----------- PROPS -----------------
{   'cluster': {},
    'input': [   's3://hboi-jobs/Pbceti_genome/01-trimmed/LP2W16W_1k_R1_001_val_1.fq.gz',
                 's3://hboi-jobs/Pbceti_genome/01-trimmed/LP2W16W_1k_R2_001_val_2.fq.gz'],
    'jobid': 0,
    'local': True,
    'log': [],
    'output': [],
    'params': {},
    'resources': {},
    'rule': 'all',
    'threads': 1,
    'type': 'single',
    'wildcards': {}}
----------- DEPS ------------------
[]
