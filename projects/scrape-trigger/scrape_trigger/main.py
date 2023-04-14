import json
import os
from typing import Dict, List

import boto3
from loguru import logger


class InvalidKeyType(Exception):
    pass


class MissingEventKey(Exception):
    pass


class PublishError(Exception):
    pass


def run(event, context):

    _validate_input(event)

    sns = boto3.client(
        service_name="sns",
        endpoint_url=os.environ.get("INFRA_ENDPOINT_URL")
    )

    search = event.get("search")
    topic_arn = os.environ["SNS_TOPIC_ARN"]

    for item in search:

        message = json.dumps({
            "search": item
        })

        try:
            sns.publish(
                TopicArn=topic_arn,
                Message=message,
            )
        except Exception as error:
            raise PublishError(error)

        logger.info(f"Message published to topic '{topic_arn}': {message}")

    return {
        "status_code": 200,
        "search": search
    }


def _validate_input(event: Dict):

    search = event.get("search")

    if not search:
        raise MissingEventKey("The 'event' argument is missing the 'search' key")

    if not isinstance(search, List):
        raise InvalidKeyType("The 'event' key 'search' must be of type list")
