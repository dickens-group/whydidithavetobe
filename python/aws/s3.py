#!/usr/bin/env python3
'''Class to simplify access to boto3 batch client
'''
__author__ = "Nick Dickens"
__copyright__ = "Copyright 2018, Nicholas J. Dickens"
__email__ = "dickensn@fau.edu"
__license__ = "MIT"

import sys
import os

import boto3
import botocore

class S3:
    def __init__(self, bucket, key, region='us-east-1'):
        '''Simplified S3 object class.
        Used to create S3 object that can be downloaded or uploaded, and have
        its size checked.
        :param bucket (str) : the S3 bucket for the file
        :param key (str) : any S3 key (path to object)
        :param region (str) : optional, defaults to us-east-1
        '''
        self.region = region
        self.set_s3()
        self.bucket = bucket
        self.key = key

    def set_s3(self):
        '''Connect the s3 client using boto3'''
        self.s3 = boto3.client('s3', self.region)

    def get_size(self):
        '''Get the S3 object content length
        :return: the size in bytes or False
        '''
        try:
            response = self.s3.head_object(Bucket=self.bucket, Key=self.key)
            return response['ContentLength']
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                # object does not exist
                #print("The object {}/{} is missing!".format(self.bucket, self.key), sys.exc_info()[0])
                return False
            else:
                # something else went wrong
                print("Could not head object: s3://{}/{}".format(self.bucket, self.key), sys.exc_info()[0])
                raise

    def upload(self, filename, overwrite=False):
        '''Check and upload the file to S3
        :param filename (str): filename for the local file
        :param overwrite (bool): (optional) overwrite if it exists, defaults to False
        '''
        if self.get_size() and overwrite==False:
            sys.exit("ERROR: cannot upload {} to s3://{}/{} because it already exists!".format(filename, self.bucket, self.key))
        else:
            self.s3.upload_file(filename, self.bucket, self.key)

    def download(self, filename, overwrite=False):
        '''Check and download the file from S3
        :param filename (str): filename for the local file
        :param overwrite (bool): (optional) overwrite if it exists, defaults to False
        '''
        if os.path.isfile(filename) and overwrite==False:
            sys.exit("ERROR: cannot download s3://{}/{} to {} because it already exists!".format(self.bucket, self.key, filename))
        else:
            if self.get_size():
                self.s3.download_file(self.bucket, self.key, filename)
            else:
                sys.exit("ERROR: cannot download s3://{}/{} - it is missing or zero bytes!".format(self.bucket, self.key, filename))

    def read(self):
        '''Read the object directly from S3 without downloading to a file'''
        s3_object = self.s3.get_object(Bucket=self.bucket, Key=self.key)
        return s3_object['Body'].read().decode('utf-8')

    def exists(self):
        '''return true if the S3 object exists '''
        if self.get_size():
            return True
        else:
            return False
            

if __name__=="__main__":
    # crude tests
    s3 = S3("whydidithavetobe","test.txt")
    assert s3.read() == "Hello World\n", "test.txt content is wrong"
    s3.download("test1.txt")
    assert os.path.exists("test1.txt") == 1, "the file was not downloaded"
    new_s3 = S3("whydidithavetobe","test1.txt")
    new_s3.upload("test1.txt")
    assert new_s3.get_size(), "the file could not be uploaded"
