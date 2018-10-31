#!/usr/bin/env python3
'''Receiving script to run snakemake in Docker
Downloads a Snakemake jobscript (--cluster) and runs it using Snakemake
'''
__author__ = "Nick Dickens"
__copyright__ = "Copyright 2018, Nicholas J. Dickens"
__email__ = "dickensn@fau.edu"
__license__ = "MIT"

from aws.s3 import S3

class Jobscript:
    def __init__(self, filename, s3_path):
        '''Jobscript class
        :param filename (str): the local filename
        :param s3_path (str): the target s3 uri string without the s3:// prefix
        '''
        self.filename = filename
        self.s3_path = s3_path
        self.bucket, sep, self.key = self.s3_path.partition("/")
        self.set_s3()

    def __str__(self):
        return "Jobscript object - filename:{} s3_path:{}".format(self.filename, self.s3_path)

    def set_s3(self):
        '''
        '''
        self.s3 = S3(self.bucket, self.key)

    def upload(self, overwrite=False):
        self.s3.upload(self.filename, overwrite=overwrite)

    def download(self, overwrite=False):
        self.s3.download(self.filename, overwrite=overwrite)

if __name__=="__main__":
    # crude test
    jobscript = Jobscript("test_jobscript.sh","whydidithavetobe/test_jobscript.sh")
    jobscript.download()
