#!/usr/bin/env python3
''' BatchRule class, to execute a single Snakemake rule as an AWS batch job
'''

__author__ = "Nick Dickens"
__copyright__ = "Copyright 2018, Nicholas J. Dickens"
__email__ = "dickensn@fau.edu"
__license__ = "MIT"

import os
import sys
import re
from argparse import ArgumentParser
from pprint import pprint

from snakemake.utils import read_job_properties


def get_target_and_snakefile(jobscript):
    target = None
    snakefile = None
    with open(jobscript) as in_fh:
        for line in in_fh:
            match_obj = re.match("-m snakemake (\S+) --snakefile (\S+) ", line)
            if match_obj:
                target=match_obj.group(1)
                snakefile=match_obj.group(2)
    if target is not None and snakefile is not None:
        return target, snakefile
    else:
        sys.exit("ERROR: could not fine target or snakefile in {}".format(jobscript))


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
    job_properties = read_job_properties(jobscript)
    target, snakefile = get_target_and_snakefile(jobscript)

    print("{}-{}-{}".format(job_properties['rule'],job_properties['jobid'],len(sys.argv)))

    with open(jobscript) as in_fh, open("job_{}.sh".format(job_properties['jobid']),"tw") as out_fh:
        for line in in_fh:
            print(line, file=out_fh)
        print("----------- PROPS -----------------", file=out_fh)
        pprint(job_properties, out_fh, indent=4)
        print("----------- DEPS ------------------", file=out_fh)
        pprint(dependencies, out_fh, indent=4)
        pprint("Target:{}".format(target), out_fh)
        pprint("Snakefile:{}".format(snakefile), out_fh)

# do something useful with the threads
#threads = job_properties[threads]

# access property defined in the cluster configuration file (Snakemake >=3.6.0)
#job_properties["cluster"]["time"]

#os.system("qsub -t {threads} {script}".format(threads=threads, script=jobscript))
