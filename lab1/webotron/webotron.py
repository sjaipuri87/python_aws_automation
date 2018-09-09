# /usr/bin/python
"""Webtron: deploys websotes with AWS
Webotron automates the process of deploying static website to s3
"""

import sys
import os
import click
import mimetypes
import platform
import boto3

from bucket import BucketManager

session = boto3.Session(profile_name='pythonAutmation')
bucket_manager = BucketManager(session)

@click.group()
def cli():
    """Webotron deploys webstites to AWS"""
    pass

@cli.command('list-buckets')
def list_buckets():
    """List all S3 buckets"""
    for bucket in bucket_manager.all_buckets():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List all objects in S3 bucket"""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket"""
    print("Creating bucket in region:", session.region_name)
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)
    return

@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET"""
    bucket_manager.sync(pathname, bucket)
    print("Website Sync is done")

if __name__ == '__main__':
    cli()
