#!/bin/sh

# properties = {"type": "single", "rule": "trim_galore", "local": false, "input": ["s3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R1_001.fastq.gz", "s3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R2_001.fastq.gz", "s3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R1_001_fastqc.zip", "s3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R2_001_fastqc.zip"], "output": ["s3://hboi-jobs/Pbceti_genome/01-trimmed/LP2W16W_1k_R1_001_val_1.fq.gz", "s3://hboi-jobs/Pbceti_genome/01-trimmed/LP2W16W_1k_R2_001_val_2.fq.gz"], "wildcards": {}, "params": {"jobQueueName": "highPriority-test-reserved", "jobDefinitionName": "trim_galore:latest"}, "log": [], "threads": 2, "resources": {"mem_mb": 4096}, "jobid": 1, "cluster": {}}

cd /home/ec2-user/water/snake_dev && \

/home/ec2-user/water/miniconda3/bin/python \

-m snakemake s3://hboi-jobs/Pbceti_genome/01-trimmed/LP2W16W_1k_R2_001_val_2.fq.gz --snakefile /home/ec2-user/water/snake_dev/simple_trim_batch.snake \

--force -j --keep-target-files --keep-remote \

--wait-for-files /home/ec2-user/water/snake_dev/.snakemake/tmp.wqg5_6p0 --latency-wait 5 \

 --attempt 1 --force-use-threads \

--wrapper-prefix https://bitbucket.org/snakemake/snakemake-wrappers/raw/ \

   --nocolor \

--notemp --no-hooks --nolock --mode 2  --allowed-rules trim_galore  && touch "/home/ec2-user/water/snake_dev/.snakemake/tmp.wqg5_6p0/1.jobfinished" || (touch "/home/ec2-user/water/snake_dev/.snakemake/tmp.wqg5_6p0/1.jobfailed"; exit 1)



----------- PROPS -----------------
{   'cluster': {},
    'input': [   's3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R1_001.fastq.gz',
                 's3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R2_001.fastq.gz',
                 's3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R1_001_fastqc.zip',
                 's3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R2_001_fastqc.zip'],
    'jobid': 1,
    'local': False,
    'log': [],
    'output': [   's3://hboi-jobs/Pbceti_genome/01-trimmed/LP2W16W_1k_R1_001_val_1.fq.gz',
                  's3://hboi-jobs/Pbceti_genome/01-trimmed/LP2W16W_1k_R2_001_val_2.fq.gz'],
    'params': {   'jobDefinitionName': 'trim_galore:latest',
                  'jobQueueName': 'highPriority-test-reserved'},
    'resources': {'mem_mb': 4096},
    'rule': 'trim_galore',
    'threads': 2,
    'type': 'single',
    'wildcards': {}}
----------- DEPS ------------------
['fastqc-2-2', 'fastqc-2-2']
