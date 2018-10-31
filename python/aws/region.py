#!/usr/bin/env python3
'''Class to simplify access to boto3 batch client
'''
__author__ = "Nick Dickens"
__copyright__ = "Copyright 2018, Nicholas J. Dickens"
__email__ = "dickensn@fau.edu"
__license__ = "MIT"

import boto3

class Region:
    def __init__(self,region=None):
        self.region = region
        self.ssm = None
        if region is None:
            self.region = self.get_from_parameter_store('default_region')

    def get_from_parameter_store(self, parameter_name):
        """
        """
        if self.ssm is None:
            self.ssm = boto3.client('ssm')
        value = None
        try:
            value = self.ssm.get_parameter(Name=parameter_name)['Parameter']['Value']
        except:
            sys.exit("ERROR: parameter {} is not available from the parameter store!".format(parameter_name))
        return value

    def get_region(self):
        return self.region


if __name__=="__main__":
    region = Region()
    print(region.get_region())
