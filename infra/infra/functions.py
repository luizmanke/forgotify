import os

import pulumi
import pulumi_aws as aws

from infra import (
    roles,
    topics
)


account_id = os.environ["AWS_ACCOUNT_ID"]
region = os.environ["AWS_REGION"]
image_tag = os.environ["AWS_IMAGE_TAG"]

config = pulumi.Config()
environment = config.require("environment")

scrape_trigger_function = aws.lambda_.Function(
    resource_name="scrape-trigger",
    environment={
        "variables": {
            "QUEUE_TOPIC_ARN": topics.query_triggered_topic.arn
        },
    },
    image_uri=f"{account_id}.dkr.ecr.{region}.amazonaws.com/scrape-trigger:{image_tag}",
    name=f"scrape-trigger-{environment}",
    package_type="Image",
    role=roles.lambda_sns_role.arn,
    timeout=60
)
