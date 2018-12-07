#!/bin/sh

# properties = {"type": "single", "rule": "fastqc", "local": false, "input": ["s3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R1_001.fastq.gz", "s3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R2_001.fastq.gz"], "output": ["s3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R1_001_fastqc.zip", "s3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R2_001_fastqc.zip"], "wildcards": {}, "params": {"jobQueueName": "highPriority-test-reserved", "jobDefinitionName": "fastqc", "jobDefinitionRevision": 28}, "log": [], "threads": 2, "resources": {"mem_mb": 4096}, "jobid": 2, "cluster": {}}

\

python \
-m snakemake hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R1_001_fastqc.zip --snakefile simple_trim_batch.snake \
--force -j --keep-target-files  \
--wait-for-files  --latency-wait 5 \
 --attempt 1 --force-use-threads \
--wrapper-prefix https://bitbucket.org/snakemake/snakemake-wrappers/raw/ \
   --nocolor \
--notemp --no-hooks --nolock --mode 2  --allowed-rules fastqc  && exit 0 || exit 1



----------- PROPS -----------------
{   'cluster': {},
    'input': [   's3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R1_001.fastq.gz',
                 's3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R2_001.fastq.gz'],
    'jobid': 2,
    'local': False,
    'log': [],
    'output': [   's3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R1_001_fastqc.zip',
                  's3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R2_001_fastqc.zip'],
    'params': {   'jobDefinitionName': 'fastqc',
                  'jobDefinitionRevision': 28,
                  'jobQueueName': 'highPriority-test-reserved'},
    'resources': {'mem_mb': 4096},
    'rule': 'fastqc',
    'threads': 2,
    'type': 'single',
    'wildcards': {}}
----------- DEPS ------------------
[]
'Target:s3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R1_001_fastqc.zip'
'Snakefile:simple_trim_batch.snake'
