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
        }
    ]

# repository check
#repo = Ecr(task_name)
repo = Ecr("snakemake-" + task_name)

build = Codebuild("whydidithavetobe-build", environment_variables)
if build.success(max_time=25):
    print("Build ok for {}.".format(build.get_name()))
else:
    print("Build failed for {}".format(build.get_name()))

