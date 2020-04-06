# shipwreck / starchart web

![starchart](https://github.com/shipwreckdev/starchart/blob/master/assets/starchart.png)

Starchart is a tool that allows you to identify and scan resources in cloud infrastructures. This iteration is the web-accessible version that runs in Django.

Under the hood, `boto3` is used to identify qualifying instances in AWS. `python-nmap` is used to facilitate scans.

## Development Notes

In its current iteration, the tool depends on [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) to provide connectivity and visibility into your account(s).

The following variables should be configured before running the tool for use with `aws`:

* `ACCESS_KEY`
* `AWS_REGION`
* `SECRET_KEY`

The long term concept behind the tool is to be able to place it into an AWS account and have it run via Fargate, ECS, EKS, or whatever other chosen method works best. This avoids the requirement for AWS credentials on a local machine.

## Requirements

* `python3`
* `django3`

## Building and Running

To start the app:

* `sudo python3 manage.py runserver`
* `python3 manage.py migrate`
* `python3 manage.py createsuperuser`

You'll need to create a user to access the app since it is gated behind authentication.

Running the app requires `sudo` usage to allow nmap to run properly.

## Update Paths

* Dockerize the app and automate the build steps mentioned above.
* Paginate large results.
* Work on adding more providers.
