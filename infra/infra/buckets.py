import pulumi
import pulumi_aws as aws


config = pulumi.Config()
environment = config.require("environment")

artists = aws.s3.Bucket(
    resource_name="artists",
    bucket=f"artists-{environment}",
    acl="private"
)
