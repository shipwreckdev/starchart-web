import boto3
import os

# AWS Credentials
ACCESS_KEY = os.getenv("ACCESS_KEY")
REGION = os.getenv("AWS_REGION")
SECRET_KEY = os.getenv("SECRET_KEY")

ec2 = boto3.resource(
    'ec2',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION,
)


def Instances():
    # Builds a list of EC2 instances with related information.

    instances = []

    for i in ec2.instances.all():
        if i.state['Name'] == 'running':
            instances.append(dict({"instance": i.instance_id, "tags": i.tags, "image": i.image_id, "src_dest": i.source_dest_check,
                                   "vpc": i.vpc_id, "public_ip": i.public_ip_address, "private_ip": i.private_ip_address}))
        else:
            continue

    return instances


def InstancePrivateIPs():
    # Builds a list of EC2 instances based on prioritizing private IP addresses.

    instance_scan_list = []

    for i in ec2.instances.all():
        if i.state['Name'] == 'running':
            instance_scan_list.append(
                dict({"instance": i.instance_id, "ip": i.private_ip_address}))
        else:
            continue

    return instance_scan_list


def InstancePublicIPs():
    # Builds a list of EC2 instances based on prioritizing private IP addresses.

    instance_scan_list = []

    for i in ec2.instances.all():
        if i.state['Name'] == 'running':
            instance_scan_list.append(
                dict({"instance": i.instance_id, "ip": i.public_ip_address}))
        else:
            continue

    return instance_scan_list


#def VPCDetails():
#    # Builds a list of VPC details.
#
#    vpcs = list(ec2.vpcs())
#    vpc_details_list = []
#
#    for v in vpcs:
#        vpc_details_list.append(dict({"id": v.id, "cidr_block": v.cidr_block}))
#
#    return vpc_details_list
#