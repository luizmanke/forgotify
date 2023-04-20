import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import boto3
from loguru import logger

from database_tools.storage import Bucket
from media_tools.schemas import Artist
from media_tools.search import Provider

from scrape_artists import exceptions


def run(event: Dict, context: Any):

    _check_inputs(event)

    artists = _get_artists(
        query=event["query"],
        media_client_id=os.environ["MEDIA_CLIENT_ID"],
        media_client_secret=os.environ["MEDIA_CLIENT_SECRET"]
    )

    _save_to_storage(
        artists,
        bucket_name=os.environ["BUCKET_NAME"],
        endpoint_url=os.environ.get("INFRA_ENDPOINT_URL")
    )

    _add_to_queue(
        artists,
        queue_name=os.environ["QUEUE_NAME"],
        endpoint_url=os.environ.get("INFRA_ENDPOINT_URL")
    )

    return {
        "status_code": 200
    }


def _check_inputs(event: Dict):

    bucket_name = os.environ.get("BUCKET_NAME")
    media_client_id = os.environ.get("MEDIA_CLIENT_ID")
    media_client_secret = os.environ.get("MEDIA_CLIENT_SECRET")
    queue_name = os.environ.get("QUEUE_NAME")
    query = event.get("query")

    if not bucket_name:
        raise exceptions.MissingEnvVar("The 'BUCKET_NAME' environment variable is missing")

    if not media_client_id:
        raise exceptions.MissingEnvVar("The 'MEDIA_CLIENT_ID' environment variable is missing")

    if not media_client_secret:
        raise exceptions.MissingEnvVar("The 'MEDIA_CLIENT_SECRET' environment variable is missing")

    if not queue_name:
        raise exceptions.MissingEnvVar("The 'QUEUE_NAME' environment variable is missing")

    if not query:
        raise exceptions.MissingEventKey("The 'event' argument is missing the 'query' key")

    if not isinstance(query, str):
        raise exceptions.InvalidKeyType("The 'event' key 'query' must be of type 'str'")


@exceptions.raise_on_failure(exceptions.GetArtistsError)
def _get_artists(
    query: str,
    media_client_id: str,
    media_client_secret: str
) -> List[Artist]:

    media_provider = Provider(
        media_client_id,
        media_client_secret
    )

    artists = media_provider.get_artists(query)
    logger.info(f"Query '{query}' returned {len(artists)} artists")

    return artists


@exceptions.raise_on_failure(exceptions.SaveToStorageError)
def _save_to_storage(
    artists: List[Artist],
    bucket_name: str,
    endpoint_url: Optional[str] = None
):
    current_time = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    bucket = Bucket(
        bucket_name,
        endpoint_url
    )

    for artist in artists:
        bucket.put_json(
            data=artist.dict(),
            file_path=f"{current_time}/{artist.id}.json"
        )

    logger.info(f"Artists saved to bucket '{bucket_name}'")


@exceptions.raise_on_failure(exceptions.AddToQueueError)
def _add_to_queue(
    artists: List[Artist],
    queue_name: str,
    endpoint_url: Optional[str] = None
):

    queue = boto3.client(
        service_name="sqs",
        endpoint_url=endpoint_url
    )

    queue_url = queue.get_queue_url(QueueName=queue_name)["QueueUrl"]

    for artist in artists:

        message = json.dumps({
            "artist": artist.name
        })

        queue.send_message(
            QueueUrl=queue_url,
            MessageBody=message,
        )

    logger.info(f"Messages added to queue '{queue_name}'")
