import json
import os
from typing import Dict, List, Optional

import boto3
from loguru import logger


def run(event, context):

    _check_input(event)

    _publish_to_topic(
        queries=event["queries"],
        queue_topic_arn=os.environ["QUEUE_TOPIC_ARN"],
        infra_endpoint_url=os.environ.get("INFRA_ENDPOINT_URL")
    )

    return {
        "status_code": 200
    }


def _check_input(event: Dict):

    queue_topic_arn = os.environ.get("QUEUE_TOPIC_ARN")
    queries = event.get("queries")

    if not queue_topic_arn:
        raise MissingEnvVar("The 'QUEUE_TOPIC_ARN' environment variable is missing")

    if not queries:
        raise MissingEventKey("The 'event' argument is missing the 'queries' key")

    if not isinstance(queries, List):
        raise InvalidKeyType("The 'event' key 'queries' must be of type list")


def _publish_to_topic(
    queries: List[str],
    queue_topic_arn: str,
    infra_endpoint_url: Optional[str]
):

    queue = boto3.client(
        service_name="sns",
        endpoint_url=infra_endpoint_url
    )

    for query in queries:

        message = json.dumps({
            "query": query
        })

        try:
            queue.publish(
                TopicArn=queue_topic_arn,
                Message=message,
            )
        except Exception as error:
            raise PublishMessageError(error)

        logger.info(f"Message published to topic '{queue_topic_arn}': {message}")


class InvalidKeyType(Exception):
    pass


class MissingEventKey(Exception):
    pass


class MissingEnvVar(Exception):
    pass


class PublishMessageError(Exception):
    pass
