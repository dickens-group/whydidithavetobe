#!/usr/bin/env python3
''' BatchRule class, to execute a single Snakemake rule as an AWS batch job
'''

__author__ = "Nick Dickens"
__copyright__ = "Copyright 2018, Nicholas J. Dickens"
__email__ = "dickensn@fau.edu"
__license__ = "MIT"

import os
import sys
from argparse import ArgumentParser
from pprint import pprint

from snakemake.utils import read_job_properties

class Job:
    def __init__(self, jobscript):
        '''
        '''
        self.job_properties = read_job_properties(jobscript)

    def check_properties(self):
        '''make sure that the job_properties dict has all the necessary parts
        for a Batch submission
        '''
        self.memory = None
        self.threads = None
        self.jobQueueName = None
        self.jobDefinitionName = None
        self.input = None
        self.output = None

    def get_properties(self):
        return self.job_properties

def get_args():
    '''collect the commandline arguments
    parameters:
        jobscript (string) : the jobscript filename
        dependencies (string) : string list of dependencies
    returns:
        argparser (dict)
    '''
    argparser = ArgumentParser()
    argparser.add_argument('--dependencies', metavar='D', type=str, nargs='+',
                help='dependencies')

    argparser.add_argument('jobscript', metavar='jobscript', type=str, nargs=1,
                help='the jobscript filename')
    return argparser.parse_args()

if __name__=="__main__":
    jobscript = sys.argv[-1]
    dependencies = sys.argv[1:-1]
    job = Job(jobscript)
    job_properties = job.get_properties()

    print("{}-{}-{}".format(job_properties['rule'],job_properties['jobid'],len(sys.argv)))

    with open(jobscript) as in_fh, open("job_{}.sh".format(job_properties['jobid']),"tw") as out_fh:
        for line in in_fh:
            print(line, file=out_fh)
        print("----------- PROPS -----------------", file=out_fh)
        pprint(job.get_properties(), out_fh, indent=4)
        print("----------- DEPS ------------------", file=out_fh)
        pprint(dependencies, out_fh, indent=4)

# do something useful with the threads
#threads = job_properties[threads]

# access property defined in the cluster configuration file (Snakemake >=3.6.0)
#job_properties["cluster"]["time"]

#os.system("qsub -t {threads} {script}".format(threads=threads, script=jobscript))
