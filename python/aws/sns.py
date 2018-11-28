#!/usr/bin/env python3
'''Class to simplify access to boto3 sns client
'''
__author__ = "Nick Dickens"
__copyright__ = "Copyright 2018, Nicholas J. Dickens"
__email__ = "dickensn@fau.edu"
__license__ = "MIT"

import sys

import boto3


class SNS:
    """Send AWS SNS notifications
    """
    def __init__(self, topicArn=None, region=None):
        if region is not None:
            self.region = region
        else:
            self.region = self.get_from_parameter_store('default_region')
        if topicArn is not None:
            self.topicArn = topicArn
        else:
            topic_name = self.get_from_parameter_store('sns_topic_name')
            account_id = self.get_from_parameter_store('account_id')
            self.topicArn = "arn:aws:sns:us-east-1:{}:{}".format(account_id, topic_name)
        self.sns = boto3.client('sns',self.region)


    def publish(self, message, subject="SNS"):
        response=self.sns.publish(TopicArn=self.topicArn, Subject=subject, Message=message)
        return response['MessageId']


if __name__ == "__main__":
    sns = SNS()
    sns.publish("Test Message")
