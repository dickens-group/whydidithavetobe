#!/bin/sh

# properties = {"type": "single", "rule": "fastqc", "local": false, "input": ["s3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R1_001.fastq.gz", "s3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R2_001.fastq.gz"], "output": ["s3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R1_001_fastqc.zip", "s3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R2_001_fastqc.zip"], "wildcards": {}, "params": {"jobQueueName": "highPriority-test-reserved", "jobDefinitionName": "fastqc:latest"}, "log": [], "threads": 2, "resources": {"mem_mb": 4096}, "jobid": 2, "cluster": {}}

cd /home/ec2-user/water/snake_dev && \

/home/ec2-user/water/miniconda3/bin/python \

-m snakemake s3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R2_001_fastqc.zip --snakefile /home/ec2-user/water/snake_dev/simple_trim_batch.snake \

--force -j --keep-target-files --keep-remote \

--wait-for-files /home/ec2-user/water/snake_dev/.snakemake/tmp.wqg5_6p0 --latency-wait 5 \

 --attempt 1 --force-use-threads \

--wrapper-prefix https://bitbucket.org/snakemake/snakemake-wrappers/raw/ \

   --nocolor \

--notemp --no-hooks --nolock --mode 2  --allowed-rules fastqc  && touch "/home/ec2-user/water/snake_dev/.snakemake/tmp.wqg5_6p0/2.jobfinished" || (touch "/home/ec2-user/water/snake_dev/.snakemake/tmp.wqg5_6p0/2.jobfailed"; exit 1)



----------- PROPS -----------------
{   'cluster': {},
    'input': [   's3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R1_001.fastq.gz',
                 's3://data-shed/test/dickens/1k_edna_reads/LP2W16W_1k_R2_001.fastq.gz'],
    'jobid': 2,
    'local': False,
    'log': [],
    'output': [   's3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R1_001_fastqc.zip',
                  's3://hboi-jobs/Pbceti_genome/00-fastqc/LP2W16W_1k_R2_001_fastqc.zip'],
    'params': {   'jobDefinitionName': 'fastqc:latest',
                  'jobQueueName': 'highPriority-test-reserved'},
    'resources': {'mem_mb': 4096},
    'rule': 'fastqc',
    'threads': 2,
    'type': 'single',
    'wildcards': {}}
----------- DEPS ------------------
[]
