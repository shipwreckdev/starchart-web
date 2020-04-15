# shipwreck / starchart web

![starchart](https://github.com/shipwreckdev/starchart-web/blob/master/assets/starchart.jpg)

Starchart is a tool that allows you to identify and scan resources in cloud infrastructures. This iteration is the web-accessible version that runs in Django.

Under the hood, `boto3` is used to identify qualifying instances in AWS. `python-nmap` is used to facilitate scans.

**Be sure** to change the password to the `starchart` user or delete it outright and create your own users before running this anywhere! We generate a default username/password of `starchart/starchart` for initial setup.

**Don't run this anywhere until you change this!**

## Requirements

* `python3`
* `django3`

## Features

Starchart provides an easy to use web interface that allows you to collect information from your AWS account.

#### Current Resource Support

* EC2 Instances
* VPCs

![starchart_vpc_info](https://github.com/shipwreckdev/starchart-web/blob/master/assets/sc_vpc_info.png)

You can also run `nmap` scans against your instances. You can pass flags for the scan direclty into the UI.

![starchart_scan_example](https://github.com/shipwreckdev/starchart-web/blob/master/assets/sc_scan_example.png)

Output is provided within the UI.

![starchart_scan_results](https://github.com/shipwreckdev/starchart-web/blob/master/assets/sc_scan_results.png)

## Authenticating to AWS

Before deploying the tool, you'll need to create a few resources within your AWS account:

* An IAM user called `starchart-web` with programmatic access credentials.
* An IAM role called `starchart-web` that provides the tool with enough credentials to get EC2 information.
* An IAM policy for the `starchart-web` user called `starchart-web-assume-role` that allows the user to assume the role `starchart-web`.

These resources are provided here for convenience.

`starchart-web-assume-role` IAM policy:

```json
{
    "Version": "2012-10-17",
    "Statement": {
        "Effect": "Allow",
        "Action": "sts:AssumeRole",
        "Resource": "arn:aws:iam::012345678901:role/starchart-web"
    }
}
```

`starchart-web` IAM role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeInstanceAttribute",
                "ec2:DescribeInstanceStatus"
                "ec2:DescribeVpcs"
            ],
            "Resource": "*"
        }
    ]
}
```

The trust relationship policy for the role should allow the `starchart-web` user to assume the role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::012345678901:user/starchart-web"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Finally, attach the `starchart-web-assume-role` permissions policy to the `starchart-web` user.

The `starchart-web` user will need programmatic access credentials. Set these matching the environment variables below on the host where the tool will be running, along with the AWS region and the AWS account ID.

These can be provided via `docker-compose.yaml` if running locally, or using something like Fargate, ECS, or EKS if running there.

All of these variables should be set:

`AWS_ACCESS_KEY_ID`
`AWS_SECRET_ACCESS_KEY`
`AWS_REGION`
`AWS_ACCOUNT_ID`

## Running the App

#### Locally From Source

Use the provided `Dockerfile` and `docker-compose.yaml` file to run the app.

Provide the four env vars listed above in `docker-compose.yaml` and run `docker-compose up`.

#### Docker Standalone

Create a `docker-compose.yaml` file similar to the one provided in this repo, with the exception of simply using the stock `starchart-web` Docker image versus building from local source:

```yaml
version: '3.2'

services:
  app:
    image: shipwreckdev/starchart-web
    environment:
      AWS_ACCESS_KEY_ID: A...
      AWS_SECRET_ACCESS_KEY: fOo...
      AWS_REGION: us-east-1
      AWS_ACCOUNT_ID: 012345678901
    ports:
      - target: 8000
        published: 8000
        protocol: tcp
        mode: host
```

With this file alone, you can run the app locally, assuming there is nothing else running on port `8000`.

#### Inside Your AWS Account

Run the tool in Fargate, ECS, or EKS. You can also optionally run the tool on an EC2 instance that has `nmap` installed and the aforementioned variables set.

## Incoming Updates

* Terraform for creating resources.
* Trying to run the VPC inspect option with no running instances throws an exception. We're working on this, but there is a dependency on building a list of running instances to generate a list of VPC IDs.
