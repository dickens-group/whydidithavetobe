#!/usr/bin/env python3
'''Class to simplify access to boto3 batch client
'''
__author__ = "Nick Dickens"
__copyright__ = "Copyright 2018, Nicholas J. Dickens"
__email__ = "dickensn@fau.edu"
__license__ = "MIT"

import sys

import boto3

from region import Region

class Job:
    '''class to connect AWS batch json
    '''
    def __init__(self, job_def, job_queue, jobId=None, revision=None, region=None):
        self.region = region
        self.set_batch()
        self.region = Region(aws_region)

        self.job_def  = job_def
        self.job_queue = job_queue
        # self.task_name = task_name
        #
        # self.filename = filename
        # self.bucket = bucket
        # self.prefix = prefix
        #
        # self.cpus = cpus
        # self.memory = memory
        #
        self.set_revision()
        # self.revision = revision
        # self.dependency = dependency
        # self.array_size = array_size
        #
        # self.set_batch()
        # self.set_jobdef()
        # self.set_jobname()
        # self.set_json()
        #
        #TODO: handle job dependencies
        # self.dependency = dependency
        self.jobName = jobName
        self.jobId = jobId

    def set_region(self):
        self.region = Region(self.region)

    def set_batch(self):
        '''connect the aws batch client'''
        self.set_region()
        self.batch = boto3.client('batch',self.region)

    def get_revision(self):
        response = self.batch.describe_job_definitions(jobDefinitionName=self.task_name)
        job_defs = response["jobDefinitions"]
        max_revision = 0
        for definition in job_defs:
            revision = definition["revision"]
            if revision >= max_revision:
                max_revision = revision

        return max_revision

    def set_jobdef(self, revision=None):
        if revision is None:
            self.revision = self.get_revision()
        else:
            self.revision = revision
        self.job_definition = "{}:{}".format(self.task_name, self.revision)

    def submit_job(self):
        response = None
        if self.dependency is not None:
            if self.array_size is not None:
                response = self.batch.submit_job(
                    jobDefinition=self.job_definition,
                    jobName=self.jobname,
                    jobQueue=self.job_queue,
                    dependsOn=self.dependency,
                    parameters={'vcpus': str(self.cpus),'memory': str(self.memory)},
                    arrayProperties={'size' : self.array_size },
                    containerOverrides={'vcpus': self.cpus,'memory': self.memory,'command': [self.json]}
                    )
            else:
                response = self.batch.submit_job(
                    jobDefinition=self.job_definition,
                    jobName=self.jobname,
                    jobQueue=self.job_queue,
                    dependsOn=self.dependency,
                    parameters={'vcpus': str(self.cpus),'memory': str(self.memory)},
                    containerOverrides={'vcpus': self.cpus,'memory': self.memory,'command': [self.json]}
                    )
        else:
            if self.array_size is not None:
                response = self.batch.submit_job(
                    jobDefinition=self.job_definition,
                    jobName=self.jobname,
                    jobQueue=self.job_queue,
                    parameters={'vcpus': str(self.cpus),'memory': str(self.memory)},
                    arrayProperties={'size' : self.array_size },
                    containerOverrides={'vcpus': self.cpus,'memory': self.memory,'command': [self.json]}
                    )
            else:
                response = self.batch.submit_job(
                    jobDefinition=self.job_definition,
                    jobName=self.jobname,
                    jobQueue=self.job_queue,
                    parameters={'vcpus': str(self.cpus),'memory': str(self.memory)},
                    containerOverrides={'vcpus': self.cpus,'memory': self.memory,'command': [self.json]}
                    )


        if 'jobId' in response:
            #is ok
            return (response['jobId'], response['jobName'])
        else:
            #throw an error
            pass


if __name__ == "__main__":
    submission = Submitter()
    submission.parse_commandline()
    submission.submit()
