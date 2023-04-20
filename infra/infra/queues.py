import pulumi
import pulumi_aws as aws


config = pulumi.Config()
environment = config.require("environment")

query_triggered = aws.sqs.Queue(
    resource_name="query-triggered",
    name=f"query-triggered-{environment}",
    visibility_timeout_seconds=300
)

artist_updated = aws.sqs.Queue(
    resource_name="artist-updated",
    name=f"artist-updated-{environment}",
    visibility_timeout_seconds=300
)
