import json

import pulumi
import pulumi_aws as aws

from infra import functions


config = pulumi.Config()
environment = config.require("environment")

monday_morning_event_rule = aws.cloudwatch.EventRule(
    resource_name="monday-morning",
    name=f"monday-morning-{environment}",
    schedule_expression="cron(0 2 ? * MON *)"
)

lambda_target = aws.cloudwatch.EventTarget(
    resource_name="monday-morning",
    arn=functions.scrape_trigger_function.arn,
    rule=monday_morning_event_rule.name,
    input=json.dumps({
        "search": ["A"]
    })
)

aws.lambda_.Permission(
    resource_name="monday-morning",
    action="lambda:InvokeFunction",
    function=functions.scrape_trigger_function.name,
    principal="events.amazonaws.com",
    source_arn=monday_morning_event_rule.arn
)
