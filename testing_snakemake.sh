aws eks create-cluster --name snakemake-dev \
--role-arn arn:aws:iam::531546992904:role/Snakemake_EKS \
--resources-vpc-config subnetIds=subnet-7742b52c,subnet-187fe07d,subnet-80f303ad,subnet-1754f45e,subnet-81dc598d,securityGroupIds=sg-f46cae8a

aws eks describe-cluster --name snakemake-dev --query cluster.status



  snakemake -s simple_trim_batch.snake --cores 4 --cluster "./batchsub.py {dependencies}" --is --notemp --no-shared-fs --cluster-status './test.py'


REMOTE=S3
PREFIX=hboi-jobs/snakemake
snakemake -s simple_trim_batch.snake \
--kubernetes --use-conda \
--default-remote-provider $REMOTE \
--default-remote-prefix $PREFIX \
-np



snakemake -s simple_trim_batch.snake \
--cores 4 \
--cluster "./batchsub.py {dependencies}" \
--is --notemp --no-shared-fs --cluster-status './test.py'


snakemake -s trim_batch_k.snake --kubernetes --use-conda \
--default-remote-provider S3 \
--default-remote-prefix hboi-jobs/kubernetes/


snakemake -s trim_batch_k.snake --kubernetes --use-singularity
