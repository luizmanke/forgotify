import json

import pulumi
import pulumi_aws as aws


config = pulumi.Config()
environment = config.require("environment")

# Reference: https://travis.media/pulumi-aws-create-lambda-sns/
scrape_trigger_role = aws.iam.Role(
    resource_name="scrape-trigger",
    name=f"scrape-trigger-{environment}",
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

scrape_artists_role = aws.iam.Role(
    resource_name="scrape-artists",
    name=f"scrape-artists-{environment}",
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

logs_create_policy = aws.iam.Policy(
    resource_name="logs-create",
    name=f"logs-create-{environment}",
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

sns_publish_policy = aws.iam.Policy(
    resource_name="sns-publish",
    name=f"sns-publish-{environment}",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sns:Publish",
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    })
)

s3_put_object_policy = aws.iam.Policy(
    resource_name="s3-put-object",
    name=f"s3-put-object-{environment}",
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
    resource_name="scrape-trigger-logs-create",
    role=scrape_trigger_role.name,
    policy_arn=logs_create_policy.arn
)

aws.iam.RolePolicyAttachment(
    resource_name="scrape-trigger-sns-publish",
    role=scrape_trigger_role.name,
    policy_arn=sns_publish_policy.arn
)

aws.iam.RolePolicyAttachment(
    resource_name="scrape-artists-logs-create",
    role=scrape_artists_role.name,
    policy_arn=logs_create_policy.arn
)

aws.iam.RolePolicyAttachment(
    resource_name="scrape-artists-s3-put-object",
    role=scrape_artists_role.name,
    policy_arn=s3_put_object_policy.arn
)

aws.iam.RolePolicyAttachment(
    resource_name="scrape-artists-sns-publish",
    role=scrape_artists_role.name,
    policy_arn=sns_publish_policy.arn
)
