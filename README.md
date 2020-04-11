# shipwreck / starchart web

![starchart](https://github.com/shipwreckdev/starchart/blob/master/assets/starchart.png)

Starchart is a tool that allows you to identify and scan resources in cloud infrastructures. This iteration is the web-accessible version that runs in Django.

Under the hood, `boto3` is used to identify qualifying instances in AWS. `python-nmap` is used to facilitate scans.

## Requirements

* `python3`
* `django3`

## Authenticating to AWS

Before deploying the tool, you'll need to create a few resources within your AWS account:

* An IAM user called `starchart-web` with programmatic access credentials.
* An IAM role called `starchart-web` that provides the tool with enough credentials to get EC2 information.
* An IAM policy for the `starchart-web` user called `starchart-web-assume-role` that allows the user to assume the role `starchart-web`.

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
            "Action": [
                "ec2:DescribeInstanceAttribute",
                "ec2:DescribeInstanceStatus",
                "ec2:DescribeInstances"
            ],
            "Effect": "Allow",
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

Take the programmatic credentials for the `starchart-web` user and make sure they are set as environment variables wherever the tool is being run.

`AWS_ACCESS_KEY_ID`
`AWS_SECRET_ACCESS_KEY`
`AWS_REGION`
`AWS_ACCOUNT_ID`

## Running the App

Use the provided `Dockerfile` and `docker-compose.yaml` file to run the app. Provide the four env vars listed above in `docker-compose.yaml` and run `docker-compose up`.
