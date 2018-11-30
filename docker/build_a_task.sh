#!/usr/bin/env bash


export account_id=531546992904
export region=us-east-1

export task_name=trim_galore
export task_version=1

echo log in to ecr
ecr_login=`aws ecr get-login --profile admin`
ecr_login=`echo $ecr_login | sed 's/-e none//'`
$ecr_login

echo build docker image

docker build -t snakemake-$task_name:$task_version -t snakemake-$task_name:latest -f snakemake-$task_name.dockerfile .

echo tag and push versions
docker tag snakemake-$task_name:$task_version $account_id.dkr.ecr.$region.amazonaws.com/snakemake-$task_name:$task_version
docker push $account_id.dkr.ecr.$region.amazonaws.com/snakemake-$task_name:$task_version
docker tag snakemake-$task_name:latest $account_id.dkr.ecr.$region.amazonaws.com/snakemake-$task_name:latest
docker push $account_id.dkr.ecr.$region.amazonaws.com/snakemake-$task_name:latest
