#! /usr/bin/python
import boto3
import os
import sys


def get_bucket_list(account):

    account = account.zfill(12)

    sts_client = boto3.client('sts')

    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    try:
        assumed_role = sts_client.assume_role(
            RoleArn="arn:aws:iam::" + account + ":role/SecurityMonkey",
            RoleSessionName="TestAssumeRole"
        )
    #  TODO Add pythonistic exception handling
    except:
        print("<<<<" + account + "AssumeRole error>>>>")
        return
    # Get temporary credentials
    credentials = assumed_role['Credentials']

    # Create connection to Amazon S3
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )
    print("\nAccount: {}".format(account))

    # Buckets Ahoy?
    for bucket in s3_resource.buckets.all():
        print("\t{}".format(bucket.name))

def get_account_list(filename):
    accounts = list()
    with open(filename) as monitored_file:
        for account in list(monitored_file):
            account = account.strip()
            if account.isdecimal():
                accounts.append(account)
    return accounts

def main():
    print (len(sys.argv))
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            for account in get_account_list(sys.argv[1]):
                get_bucket_list(account)
        else:
            get_bucket_list(sys.argv[1])


print(__name__)
if __name__ == "__main__":
    main()

