import json
import os
from typing import List

import boto3


class MissingEventKey(Exception):
    pass


class InvalidKeyType(Exception):
    pass


def run(event, context):

    search = event.get("search")

    if not search:
        raise MissingEventKey("The 'event' argument is missing the 'search' key")

    if not isinstance(search, List):
        raise InvalidKeyType("The 'event' key 'search' must be of type list")

    sns = boto3.client(
        service_name="sns",
        endpoint_url=os.environ.get("INFRA_ENDPOINT_URL")
    )

    for item in search:
        sns.publish(
            TopicArn=os.environ["SNS_TOPIC_ARN"],
            Message=json.dumps({
                "search": item
            }),
        )

    return {
        "status_code": 200,
        "search": search
    }
