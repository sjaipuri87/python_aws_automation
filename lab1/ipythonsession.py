# coding: utf-8
import boto3
cat C:/Users/sjaipuri/.aws/config
cat ~/.aws/config
cat ../../.aws/config
get_ipython().run_line_magic('ls', '')
locate .aws
session = boto3.Session(profile_name='pythoAutmation')
session = boto3.Session(profile_name='pythonAutmation')
s3 = session.resource('s3')
for bucket in s3.buckets.all():
    print(bucket)
    
for bucket in s3.buckets.all():
    print(bucket)
    
new_bucket = s3.create_bucket(Bucket='automationbucket-boto3sj')
new_bucket = s3.create_bucket(Bucket='automationbucket-boto3sj', CreateBucketConfiguration={'LocationConstraint":us-west-1})) 
new_bucket = s3.create_bucket(Bucket='automationbucket-boto3sj', CreateBucketConfiguration={'LocationConstraint':us-west-1})) 
new_bucket = s3.create_bucket(Bucket='automationbucket-boto3sj', CreateBucketConfiguration={'LocationConstraint':us-west-1})
new_bucket = s3.create_bucket(Bucket='automationbucket-boto3sj', CreateBucketConfiguration={'LocationConstraint':'us-west-1'})
for bucket in s3.buckets.all():
    print(bucket)
    
get_ipython().run_line_magic('history', '')
