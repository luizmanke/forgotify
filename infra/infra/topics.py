import pulumi
import pulumi_aws as aws


config = pulumi.Config()
environment = config.require("environment")

scrape_artist_topic = aws.sns.Topic(
    "scrape-artist",
    name=f"scrape-artist-{environment}"
)