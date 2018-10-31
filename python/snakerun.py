#!/usr/bin/env python3
'''Receiving script to run snakemake in Docker
Downloads a Snakemake jobscript (--cluster) and runs it using Snakemake
'''
__author__ = "Nick Dickens"
__copyright__ = "Copyright 2018, Nicholas J. Dickens"
__email__ = "dickensn@fau.edu"
__license__ = "MIT"

import sys
import os
from uuid import uuid4

import boto3

class Jobscript:
    def __init__(self, s3_path):
        self.s3_path = s3_path
        self.filename = self.s3_path.rpartition("/")[2]

    def __str__(self):
        return "Jobscript object, path:{} filename:{}".format(self.s3_path, self.filename)


def unique_dir(base_path=""):
    '''Creates a unique working directory in case of multiple
    occupancy of the docker host
    :param base_path: (optional) base path for the directory
    :return: a unique folder in base_path using uuid
    '''
    dir_name = os.path.join(base_path, str(uuid4()))
    try:
        os.mkdir(dir_name)
    except Exception as e:
        print("Could not make the directory: {}".format(dir_name), sys.exc_info()[0])
        raise
    return dir_name
