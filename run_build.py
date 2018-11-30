#!/usr/bin/env python3

import json
import sys

from codebuild import Codebuild
from ecr import Ecr


if len(sys.argv)<2:
    sys.exit("ERROR: you must specify a task name!")
task_name = sys.argv[1]


task_version = 1
if len(sys.argv) > 2:
    task_version = sys.argv[2]

json_file = "test/test-{}.json".format(task_name)

with open(json_file) as json_fh:
    json_data = json.load(json_fh)

memory = json_data.get("memory", None)
threads = json_data.get("threads", None)

if memory is None:
    sys.exit("ERROR: json file {} does not contain a memory entry!".format(json_file))

if threads is None:
    sys.exit("ERROR: json file {} does not contain an entry for threads!".format(json_file))

environment_variables= [
        {
        "name" : "task_name",
        "value" : task_name,
        "type" : "PLAINTEXT"
        },
        {
        "name" : "task_version",
        "value" : str(task_version),
        "type" : "PLAINTEXT"
        },
        {
        "name" : "memory",
        "value" : str(memory),
        "type" : "PLAINTEXT"
        },
        {
            "name" : "threads",
            "value" : str(threads),
            "type" : "PLAINTEXT"
        }
    ]

# repository check
repo = Ecr(task_name)

build = Codebuild("hboi-jobs-build-task", environment_variables)
if build.success(max_time=25):
    test_build = Codebuild("hboi-jobs-test-task", environment_variables)
    if test_build.success(max_time=30):
        pass
    else:
        print("Build failed for {}".format(test_build.get_name()))
else:
    print("Build failed for {}".format(build.get_name()))

# retrieve batch submission and add job notification
