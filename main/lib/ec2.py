import boto3
import os
from .assume_role import assume_aws_role

account_id = os.getenv("AWS_ACCOUNT_ID")
role_name = "starchart-web"

# Fetch credentials using STS.

credentials = assume_aws_role(account_id, role_name)

# Establish EC2 resource.

ec2 = boto3.resource(
    'ec2',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken'],
    region_name=os.getenv('AWS_REGION')
)


def Instances():
    """Builds a list of EC2 instances with related information."""

    instances = []

    for i in ec2.instances.all():
        if i.state['Name'] == 'running':
            instances.append(dict({"instance": i.instance_id, "tags": i.tags, "image": i.image_id, "src_dest": i.source_dest_check,
                                   "vpc": i.vpc_id, "public_ip": i.public_ip_address, "private_ip": i.private_ip_address}))
        else:
            continue

    return instances


def InstancePrivateIPs():
    """Builds a list of EC2 instances based on prioritizing private IP addresses."""

    instance_scan_list = []

    for i in ec2.instances.all():
        if i.state['Name'] == 'running':
            instance_scan_list.append(
                dict({"instance": i.instance_id, "ip": i.private_ip_address}))
        else:
            continue

    return instance_scan_list


def InstancePublicIPs():
    """Builds a list of EC2 instances based on prioritizing private IP addresses."""

    instance_scan_list = []

    for i in ec2.instances.all():
        if i.state['Name'] == 'running':
            instance_scan_list.append(
                dict({"instance": i.instance_id, "ip": i.public_ip_address}))
        else:
            continue

    return instance_scan_list


def VPCDetails(vpc_list):
    """Builds a list of VPC details."""
    vpc_details_list = []

    for v in vpc_list:
        vpc = ec2.Vpc(v)

        vpc_details_list.append(
            dict({"id": vpc.vpc_id, "cidr_block": vpc.cidr_block, "state": vpc.state, "instance_tenancy": vpc.instance_tenancy}))

    return vpc_details_list
