import os
from typing import Dict, List, Optional

from loguru import logger

from cloud_tools.messenger import Queue


def run(event, context) -> Dict:

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
        raise MissingEnvVar("The 'QUEUE_NAME' environment variable is missing")

    if not queries:
        raise MissingEventKey("The 'event' argument is missing the 'queries' key")

    if not isinstance(queries, List):
        raise InvalidKeyType("The 'event' key 'queries' must be of type list")


def _add_to_queue(
    queries: List[str],
    queue_name: str,
    endpoint_url: Optional[str] = None
):
    queue = Queue(
        queue_name,
        endpoint_url
    )

    for query in queries:
        message = {"query": query}
        queue.add_json(message)

    logger.info(f"{len(queries)} messages added to queue '{queue_name}'")


class InvalidKeyType(Exception):
    pass


class MissingEnvVar(Exception):
    pass


class MissingEventKey(Exception):
    pass
