import json
import os
from typing import Dict, List, Optional

import boto3
from loguru import logger

from scrape_trigger import exceptions


def run(event, context):

    _check_input(event)

    _add_to_queue(
        queries=event["queries"],
        queue_name=os.environ["QUEUE_NAME"],
        endpoint_url=os.environ.get("INFRA_ENDPOINT_URL")
    )

    return {
        "status_code": 200
    }


def _check_input(event: Dict):

    queue_name = os.environ.get("QUEUE_NAME")
    queries = event.get("queries")

    if not queue_name:
        raise exceptions.MissingEnvVar("The 'QUEUE_NAME' environment variable is missing")

    if not queries:
        raise exceptions.MissingEventKey("The 'event' argument is missing the 'queries' key")

    if not isinstance(queries, List):
        raise exceptions.InvalidKeyType("The 'event' key 'queries' must be of type list")


@exceptions.raise_on_failure(exceptions.AddToQueueError)
def _add_to_queue(
    queries: List[str],
    queue_name: str,
    endpoint_url: Optional[str] = None
):

    queue = boto3.client(
        service_name="sqs",
        endpoint_url=endpoint_url
    )

    queue_url = queue.get_queue_url(QueueName=queue_name)["QueueUrl"]

    for query in queries:

        message = json.dumps({
            "query": query
        })

        queue.send_message(
            QueueUrl=queue_url,
            MessageBody=message,
        )

    logger.info(f"{len(queries)} messages added to queue '{queue_name}'")
