import json

import pulumi
import pulumi_aws as aws


config = pulumi.Config()
environment = config.require("environment")

# Reference: https://travis.media/pulumi-aws-create-lambda-sns/
lambda_sns_role = aws.iam.Role(
    resource_name="lambda-sns",
    name=f"lambda-sns-{environment}",
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
    
aws.iam.RolePolicyAttachment(
    resource_name="lambda-sns-publish",
    role=lambda_sns_role.name,
    policy_arn=sns_publish_policy.arn
)
