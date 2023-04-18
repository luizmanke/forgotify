import os

import pulumi
import pulumi_aws as aws

from infra import (
    buckets,
    roles,
    topics
)


account_id = os.environ["AWS_ACCOUNT_ID"]
region = os.environ["AWS_REGION"]
image_tag = os.environ["AWS_IMAGE_TAG"]

config = pulumi.Config()
environment = config.require("environment")
media_client_id = config.require_secret("media_client_id")
media_client_secret = config.require_secret("media_client_secret")

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
    role=roles.scrape_trigger_role.arn,
    timeout=60
)

scrape_artists_function = aws.lambda_.Function(
    resource_name="scrape-artists",
    environment={
        "variables": {
            "BUCKET_NAME": buckets.artists_bucket.bucket,
            "MEDIA_CLIENT_ID": media_client_id,
            "MEDIA_CLIENT_SECRET": media_client_secret,
            "QUEUE_TOPIC_ARN": topics.query_triggered_topic.arn
        },
    },
    image_uri=f"{account_id}.dkr.ecr.{region}.amazonaws.com/scrape-artists:{image_tag}",
    name=f"scrape-artists-{environment}",
    package_type="Image",
    role=roles.scrape_artists_role.arn,
    timeout=300
)
