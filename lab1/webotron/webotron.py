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

from botocore.exceptions import ClientError
from pathlib import Path


session = boto3.Session(profile_name='pythonAutmation')
s3 = session.resource('s3')

@click.group()
def cli():
    """Webotron deploys webstites to AWS"""
    pass

@cli.command('list-buckets')
def list_buckets():
    """List all S3 buckets"""
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List all objects in S3 bucket"""
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket"""
    print("Creating bucket in region:", session.region_name)
    s3_bucket = None
    try:
        s3_bucket = s3.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={'LocationConstraint': session.region_name}
        )
    except ClientError as err:
        if err.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)
            print("Bucket is already owned by you")
        else:
            raise err

    policy = """
    {
      "Version":"2012-10-17",
      "Statement":[{
      "Sid":"PublicReadGetObject",
      "Effect":"Allow",
      "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::%s/*"
          ]
        }
      ]
    }
    """ % s3_bucket.name
    policy = policy.strip()
    pol = s3_bucket.Policy()
    pol.put(Policy=policy)
    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={
        'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    })
    return

def upload_file(s3_bucket, path, key):
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    s3_bucket.upload_file(
        path,
        key,
        ExtraArgs={
        'ContentType': content_type
        })

def convertPath(path):
    separator = os.path.sep
    # print(separator)
    if separator != '/':
        path = path.replace(separator, '/')
    return path

@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET"""
    s3_bucket = s3.Bucket(bucket)
    root = Path(pathname).expanduser().resolve()
    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir():
                handle_directory(p)
            if p.is_file():
                upload_file(s3_bucket, str(p), convertPath(str(p.relative_to(root))))  # Using convert path to hand windows dir
                # print("Path: {}\n Key: {}".format(p, p.relative_to(root)))
    print("Website Sync is done")

    handle_directory(root)


if __name__ == '__main__':
    cli()
