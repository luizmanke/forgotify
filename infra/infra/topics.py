import pulumi
import pulumi_aws as aws


config = pulumi.Config()
environment = config.require("environment")

query_triggered_topic = aws.sns.Topic(
    resource_name="query-triggered",
    name=f"query-triggered-{environment}"
)
