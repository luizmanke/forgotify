import json
import os

import pulumi
import pulumi_aws as aws

from infra import (
    buckets,
    queues
)


account_id = os.environ["AWS_ACCOUNT_ID"]
region = os.environ["AWS_REGION"]
image_tag = os.environ["AWS_IMAGE_TAG"]

config = pulumi.Config()
environment = config.require("environment")
media_client_id = config.require_secret("media_client_id")
media_client_secret = config.require_secret("media_client_secret")

########
# ROLE #
########

lambda_role = aws.iam.Role(
    resource_name="scrape-tracks-role",
    name=f"scrape-tracks-role-{environment}",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com",
                },
                "Effect": "Allow",
                "Sid": "",
            }
        ]
    })
)

logs_policy = aws.iam.Policy(
    resource_name="scrape-tracks-logs-policy",
    name=f"scrape-tracks-logs-policy-{environment}",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "*"
            }
        ]
    })
)

aws.iam.RolePolicyAttachment(
    resource_name="scrape-tracks-logs-policy-attachment",
    role=lambda_role.name,
    policy_arn=logs_policy.arn
)

s3_policy = aws.iam.Policy(
    resource_name="scrape-tracks-s3-policy",
    name=f"scrape-tracks-s3-policy-{environment}",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "s3:PutObject",
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    })
)

aws.iam.RolePolicyAttachment(
    resource_name="scrape-tracks-s3-policy-attachment",
    role=lambda_role.name,
    policy_arn=s3_policy.arn
)

sqs_policy = aws.iam.Policy(
    resource_name="scrape-tracks-sqs-policy",
    name=f"scrape-tracks-sqs-policy-{environment}",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "sqs:DeleteMessage",
                    "sqs:GetQueueAttributes",
                    "sqs:GetQueueUrl",
                    "sqs:ReceiveMessage"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    })
)

aws.iam.RolePolicyAttachment(
    resource_name="scrape-tracks-sqs-policy-attachment",
    role=lambda_role.name,
    policy_arn=sqs_policy.arn
)

##########
# LAMBDA #
##########

lambda_function = aws.lambda_.Function(
    resource_name="scrape-tracks-function",
    name=f"scrape-tracks-function-{environment}",
    environment={
        "variables": {
            "BUCKET_NAME": buckets.tracks.bucket,
            "MEDIA_CLIENT_ID": media_client_id,
            "MEDIA_CLIENT_SECRET": media_client_secret
        },
    },
    image_uri=f"{account_id}.dkr.ecr.{region}.amazonaws.com/scrape-tracks:{image_tag}",
    package_type="Image",
    role=lambda_role.arn,
    timeout=300
)

###########
# TRIGGER #
###########

aws.lambda_.EventSourceMapping(
    resource_name="scrape-tracks-event-source-mapping",
    event_source_arn=queues.artist_updated.arn,
    function_name=lambda_function.arn
)
