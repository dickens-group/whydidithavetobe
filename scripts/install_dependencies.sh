#!/usr/bin/env bash

user_dir="/home/ec2-user/.miniconda3"

#check if conda is already there
keep_output=`conda info`
status=$?

if [[ $status -eq 1 ]]; then
  curl -o miniconda3.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
  mkdir -p $user_dir
  bash miniconda3.sh -f -b -p $user_dir
  rm -f miniconda3.sh
  chmod -R +x $user_dir/bin/
  echo "PATH=\"$user_dir/bin:\$PATH\"" >> /home/ec2-user/.bashrc
  sudo -u ec2-user conda config --add channels conda-forge
  sudo -u ec2-user conda config --add channels defaults
  sudo -u ec2-user conda config --add channels bioconda
  sudo -u ec2-user conda install -y snakemake boto3
else
  # check snakemake is there
  result=`conda list | grep snakemake | cut -f 1 -d " "`
  if [[ $result -eq "snakemake" ]]; then
    echo "snakemake environment already exists"
  else
    conda install -y snakemake python=3
  fi

  # check boto3
  result=`conda list | grep boto3 | cut -f 1 -d " "`
  if [[ $result -eq "boto3" ]]; then
    echo "snakemake environment already exists"
  else
    conda install -y snakemake python=3
  fi
fi
