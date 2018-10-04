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

from submit import Submitter

class BatchRule:
    ''' BatchRule class
    '''
    def __init__(self, cmd, task_name, input_data, output_data, threads, memory,
                 array_job, queue, bucket, prefix, output_name, overwrite=False,
                 first_step=False, reference=None):
        self.command = cmd
        self.task_name = task_name
        self.input_data = input_data
        self.output_data = output_data
        self.threads = threads
        self.memory = memory
        self.array_job = array_job
        self.queue = queue
        self.bucket = bucket
        self.prefix = prefix
        self.output_name = output_name
        self.overwrite = overwrite
        self.reference = reference

        self.first_step = first_step
        self.jobIds = None
        self.dependencies = []

        self.read_input()
        if self.reference is not None:
            self.set_reference()
        self.read_output()
        self.read_dependencies()
        self.assemble_json_data()


    def __str__(self):
        return "BatchRule:\n----------\n\tcmd:{}\n\ttask_name:{}\n\tthreads:{}\n\tmemory:{}\n\tqueue:{}\n\tarray_job:{}\n\tinput:{}\n\toutput:{}\n\tbucket:{}\n\tprefix:{}\toutput_name:{}\n\toverwrite:{}\n\treference:{}\n\n".format(
            self.command, self.task_name, self.input_data, self.output_data, self.threads,
            self.memory, self.array_job, self.queue, self.bucket, self.prefix, self.output_name, self.overwrite, self.reference)

    def read_input(self):
        ''' convert the input dict into a list of the input files
        '''
        if "manifest" in self.input_data:
            self.manifest = self.input_data['manifest']
            self.manifest_to_samples()
        elif "manifest" in self.command:
            # assume it is the first value if there is a manifest in the command
            self.manifest = self.input_data[0]
            self.manifest_to_samples()
        else:
            # if there isn't a manifest load all the files in input into a the samples
            self.samples = []
            for filename in self.input_data:
                #load the data from input_data
                sample = {}
                (name, sep, suffix) = filename.rpartition(".")
                sample['name'] = name
                # the input for all steps apart from step 1 should be in this prefix
                sample['prefix'] = self.prefix + "/" + self.output_name
                sample['bucket'] = self.bucket
                sample['files'] = []
                sample['files'].append(filename)
                self.samples.append(sample)

    def read_output(self):
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

    def manifest_to_samples(self):
        self.samples = []
        self.samples_dict = {}
        # if it is a manifest file then it is the first step (qiime2)
        self.first_step = True
        with open(self.manifest) as manifest_fh:
            next(manifest_fh)
            for line in manifest_fh:
                (sample_id,filepath,direction) = line.split(",")
                (bucket, sep, filepath) = filepath.partition("/")
                (prefix, sep, filename) = filepath.rpartition("/")
                if sample_id in self.samples_dict:
                    self.samples_dict[sample_id]['files'].append(filename)
                else:
                    sample = {}
                    sample['name'] = sample_id
                    sample['bucket'] = bucket
                    sample['prefix'] = prefix
                    sample['files'] = []
                    sample['files'].append(filename)
                    self.samples_dict[sample_id] = sample
                #sort the files list into order, should make sure that R1 is first
                self.samples_dict[sample_id]['files'].sort()

        for sample_id in self.samples_dict:
            self.samples.append(self.samples_dict[sample_id])

    def write_json(self):
        '''write the json data to a file
        '''
        #take the first 2 words from the command
        prefix = "-".join(self.command.split(" ")[:2])
        # add a unique ID
        self.json_file = prefix + "-" + str(uuid4())

        with open(self.json_file, "w") as json_fh:
            json.dump(self.json_data, json_fh)

    def read_dependencies(self):
        ''' if this isn't the rule step in the snakefile the input files will
        contain jobIds
        '''
        if not self.first_step:
            jobIds = set()
            for filename in self.input_data:
                this_id = self.read_jobId(filename)
                if this_id is not None and this_id != "":
                    jobIds.add(this_id)
            self.jobIds = jobIds
            for jobId in self.jobIds:
                dependency = {}
                dependency['jobId'] = jobId
                self.dependencies.append(dependency)
        # print("---------------")
        # pprint(self.dependencies, indent=4)

    def read_jobId(self, filename):
        ''' each file will contain 1 jobId
        '''
        jobId = None
        with open(filename) as in_fh:
            jobId = in_fh.readline().rstrip()
        return jobId

    def submit_job(self):
        ''' submit the json file as an aws batch job
        '''
        # set the self.jobId
        submission = Submitter(filename=self.json_file, bucket=self.bucket,
                               prefix=self.prefix, is_s3=False,
                               json=self.json_file, s3_overwrite=False,
                               region="us-east-1", queue=self.queue)
        self.submission_jobId = submission.submit()
        # print("****" + self.submission_jobId)

    def write_output_files(self):
        ''' on successful job submission write the jobId to all of the
        output files
        '''
        for filename in self.output_data:
            with open(filename, "w") as out_fh:
                print(self.submission_jobId, file=out_fh)

    def submit(self):
        self.write_json()
        self.submit_job()
        self.write_output_files()


if __name__ == "__main__":
    input_data = {"manifest" : "manifest.csv"}
    output_data = {"seqs" : "paired-end-demux.qza"}
    params = {}
    rule = BatchRule(cmd="tools import --type SampleData[PairedEndSequencesWithQuality] --input-path manifest.csv --output-path paired-end-demux.qza --source-format PairedEndFastqManifestPhred33",
                     task_name="qiime2", threads=1, memory=2048, queue="highPriority-test-reserved", array_job=False,
                     input_data=input_data, output_data=output_data,
                     bucket="hboi-jobs", prefix="hurricane", output_name="dev",
                     overwrite=True, reference=None
                     )
    print(rule)
