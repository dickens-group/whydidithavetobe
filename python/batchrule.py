#!/usr/bin/env python3
''' BatchRule class, to execute a single Snakemake rule as an AWS batch job
'''

__author__ = "Nick Dickens"
__copyright__ = "Copyright 2018, Nicholas J. Dickens"
__email__ = "dickensn@fau.edu"
__license__ = "MIT"

import sys
import json

from uuid import uuid4


class BatchRule:
    ''' BatchRule class
    inputs are in the s3 format bucket/prefix/key.txt, but it
    writes and reads local files - e.g. key.txt
    '''
    def __init__(self, cmd, inputs, outputs,
                 threads, memory, job_def, job_queue, array_job=False,
                 overwrite=False, first_step=False):
        self.command = cmd
        self.inputs = inputs
        self.outputs = outputs

        self.threads = threads
        self.memory = memory
        self.job_def = job_def
        self.job_queue = job_queue
        self.array_job = array_job

        self.overwrite = overwrite
        self.first_step = first_step

        self.dependencies = set()
        self.jobIds = set()

        self.read_inputs()


    def __str__(self):
        return """
        BatchRule:
        ----------
        cmd:{}
        inputs:{}
        outputs:{}
        threads:{}, memory:{}
        job_def:{}, queue:{}, array_job:{}
        overwrite:{}
        first_step:{}
        """.format(
            self.command, ",".join(self.inputs), ",".join(self.outputs),
            self.threads, self.memory, self.job_def, self.job_queue, self.array_job,
            self.overwrite, self.first_step)

    def read_inputs(self):
        ''' read the input list and check for dependencies
        '''
        #TODO: check input exists
        if not self.first_step:
            for entry in self.inputs:
                (bucket, sep, key) = entry.partition("/")
                (prefix, sep, filename) = key.rpartition("/")
                self.read_dependencies(filename)




    def write_outputs(self):
        ''' convert the output dict into a list of the output files
        '''
        self.output = {}
        self.output['name'] = self.output_name
        self.output['prefix'] = self.prefix
        self.output['bucket'] = self.bucket
        self.output['overwrite'] = self.overwrite
        output_files = []
        for filename in self.output_data:
            output_files.append(filename)
        self.output['files'] = output_files

    def set_reference(self):
        ''' not yet implemented
        '''
        pass

    def assemble_json_data(self):
        ''' puts the data into a format suitable for job submission using
            the lab workflows
        '''
        self.json_data = {}
        self.json_data['input'] = {}
        self.json_data['input']['samples'] = self.samples
        if self.reference is not None:
            self.json_data['input']['reference'] = self.reference
        self.json_data['output'] = self.output
        self.json_data['task'] = self.task_name
        self.json_data['threads'] = self.threads
        self.json_data['memory'] = self.memory
        self.json_data['opts'] = {}
        self.json_data['opts'][self.task_name] = self.command
        if len(self.dependencies)>0:
            self.json_data['dependency'] = self.dependencies


    def write_json(self):
        ''' write the json data to a unique file
        '''
        # take the first 2 words from the command
        prefix = "-".join(self.command.split(" ")[:2])
        # add a unique ID
        self.json_file = prefix + "-" + str(uuid4())

        with open(self.json_file, "w") as json_fh:
            json.dump(self.json_data, json_fh)


    def read_dependencies(self, filename):
        ''' if this isn't the rule step in the snakefile the input files will
        contain jobIds
        '''
        with open(filename) as in_fh:
            for line in in_fh:
                id = line.rstrip()
                self.dependencies.add(id)


    def submit_job(self):
        ''' submit the json file as an aws batch job
        '''
        # set the self.jobId
        # submission = Submitter(filename=self.json_file, bucket=self.bucket,
        #                        prefix=self.prefix, is_s3=False,
        #                        json=self.json_file, s3_overwrite=False,
        #                        region="us-east-1", queue=self.queue)
        # self.submission_jobId = submission.submit()
        # print("****" + self.submission_jobId)
        #
        # jobIds.add(batch.submit_job())
        pass

    def write_outputs(self):
        ''' on successful job submission write the jobId to all of the
        output files
        '''
        for entry in self.outputs:
            (bucket, sep, key) = entry.partition("/")
            (prefix, sep, filename) = key.rpartition("/")
            with open(filename, "w") as out_fh:
                print("\n".join(list(self.jobIds)), file=out_fh)

    def submit(self):
        self.write_json()
        self.submit_job()
        self.write_outputs()


if __name__ == "__main__":
    inputs = ["manifest.csv"]
    outputs = ["paired-end-demux.qza"]

    rule = BatchRule(cmd="qiime2 tools import --type SampleData[PairedEndSequencesWithQuality] --input-path manifest.csv --output-path paired-end-demux.qza --source-format PairedEndFastqManifestPhred33",
                     inputs=inputs, outputs=outputs,
                     threads=1, memory=2048, job_def="", job_queue="highPriority-test-reserved", array_job=False,
                     overwrite=True, first_step=True
                     )
    print(rule)
