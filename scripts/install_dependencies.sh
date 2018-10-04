#!/usr/bin/env bash

#TODO: is conda installed?

# check the environment
result=`conda info --env | grep snakemake | cut -f 1 -d " "`

if [[ $result -eq "snakemake" ]]; then
  echo "snakemake environment already exists"
else
  conda create -n snakemake python=3 snakemake boto3 -y
fi
