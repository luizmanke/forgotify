import os

import pulumi
import pulumi_aws as aws

from infra import roles


account_id = os.environ["AWS_ACCOUNT_ID"]
region = os.environ["AWS_REGION"]
image_tag = os.environ.get("AWS_IMAGE_TAG", "dev")

config = pulumi.Config()
environment = config.require("environment")

aws.lambda_.Function(
    "scrape-trigger",
    image_uri=f"{account_id}.dkr.ecr.{region}.amazonaws.com/scrape-trigger:{image_tag}",
    name=f"scrape-trigger-{environment}",
    package_type="Image",
    role=roles.lambda_sns_role.arn,
    timeout=60
)