import boto3

sts_client = boto3.client('sts')


def assume_aws_role(account_id, role_name):
    assumed_role_object = sts_client.assume_role(
        RoleArn="arn:aws:iam::{}:role/{}".format(account_id, role_name),
        RoleSessionName="starchart-web"
    )

    credentials = assumed_role_object['Credentials']

    return credentials
