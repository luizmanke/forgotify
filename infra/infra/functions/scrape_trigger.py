import json
import os

import pulumi
import pulumi_aws as aws

from infra import queues


account_id = os.environ["AWS_ACCOUNT_ID"]
region = os.environ["AWS_REGION"]
image_tag = os.environ["AWS_IMAGE_TAG"]

config = pulumi.Config()
environment = config.require("environment")

########
# ROLE #
########

lambda_role = aws.iam.Role(
    resource_name="scrape-trigger-role",
    name=f"scrape-trigger-role-{environment}",
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
    resource_name="scrape-trigger-logs-policy",
    name=f"scrape-trigger-logs-policy-{environment}",
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
    resource_name="scrape-trigger-logs-policy-attachment",
    role=lambda_role.name,
    policy_arn=logs_policy.arn
)

sqs_policy = aws.iam.Policy(
    resource_name="scrape-trigger-sqs-policy",
    name=f"scrape-trigger-sqs-policy-{environment}",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sqs:SendMessage",
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    })
)

aws.iam.RolePolicyAttachment(
    resource_name="scrape-trigger-sqs-policy-attachment",
    role=lambda_role.name,
    policy_arn=sqs_policy.arn
)

##########
# LAMBDA #
##########

lambda_function = aws.lambda_.Function(
    resource_name="scrape-trigger-function",
    name=f"scrape-trigger-function-{environment}",
    environment={
        "variables": {
            "QUEUE_NAME": queues.query_triggered.name
        },
    },
    image_uri=f"{account_id}.dkr.ecr.{region}.amazonaws.com/scrape-trigger:{image_tag}",
    package_type="Image",
    role=lambda_role.arn,
    timeout=60
)

###########
# TRIGGER #
###########

event_rule = aws.cloudwatch.EventRule(
    resource_name="scrape-trigger-event-rule",
    name=f"scrape-trigger-event-rule-{environment}",
    schedule_expression="cron(0 2 ? * MON *)"
)

lambda_target = aws.cloudwatch.EventTarget(
    resource_name="scrape-trigger-event-target",
    arn=lambda_function.arn,
    rule=event_rule.name,
    input=json.dumps({
        "search": ["A"]
    })
)

aws.lambda_.Permission(
    resource_name="scrape-trigger-event-permission",
    action="lambda:InvokeFunction",
    function=lambda_function.name,
    principal="events.amazonaws.com",
    source_arn=event_rule.arn
)
