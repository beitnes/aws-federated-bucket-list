#! /usr/bin/python
import boto3
import sys


def get_bucket_list(account):
    sts_client = boto3.client('sts')

    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    assumed_role = sts_client.assume_role(
        RoleArn="arn:aws:iam::" + account + ":role/SecurityMonkey",
        RoleSessionName="TestAssumeRole"
    )

    # Get temporary credentials
    credentials = assumed_role['Credentials']

    # Create connection to Amazon S3
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    # Buckets Ahoy?
    for bucket in s3_resource.buckets.all():
        print(bucket.name)


def main():
    if len(sys.argv) == 3:
        print(sys.argv[1])
        get_bucket_list(sys.argv[1])


print(__name__)
if __name__ == "__main__":
    main()

