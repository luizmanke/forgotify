import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import boto3
from loguru import logger

from media_tools.schemas import Artist
from media_tools.search import Provider


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
        infra_endpoint_url=os.environ.get("INFRA_ENDPOINT_URL")
    )

    _publish_to_topic(
        artists,
        queue_topic_arn=os.environ["QUEUE_TOPIC_ARN"],
        infra_endpoint_url=os.environ.get("INFRA_ENDPOINT_URL")
    )

    return {
        "status_code": 200
    }


def _check_inputs(event: Dict):

    bucket_name = os.environ.get("BUCKET_NAME")
    media_client_id = os.environ.get("MEDIA_CLIENT_ID")
    media_client_secret = os.environ.get("MEDIA_CLIENT_SECRET")
    queue_topic_arn = os.environ.get("QUEUE_TOPIC_ARN")
    query = event.get("query")

    if not bucket_name:
        raise MissingEnvVar("The 'BUCKET_NAME' environment variable is missing")

    if not media_client_id:
        raise MissingEnvVar("The 'MEDIA_CLIENT_ID' environment variable is missing")

    if not media_client_secret:
        raise MissingEnvVar("The 'MEDIA_CLIENT_SECRET' environment variable is missing")

    if not queue_topic_arn:
        raise MissingEnvVar("The 'QUEUE_TOPIC_ARN' environment variable is missing")

    if not query:
        raise MissingEventKey("The 'event' argument is missing the 'query' key")

    if not isinstance(query, str):
        raise InvalidKeyType("The 'event' key 'query' must be of type 'str'")


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


def _save_to_storage(
    artists: List[Artist],
    bucket_name: str,
    infra_endpoint_url: Optional[str]
):
    current_time = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    storage = boto3.client(
        service_name="s3",
        endpoint_url=infra_endpoint_url
    )

    for artist in artists:

        try:
            storage.put_object(
                Body=json.dumps(artist.dict()),
                Bucket=bucket_name,
                Key=f"{artist.id}_{current_time}.json"
            )
        except Exception as error:
            raise SaveToStorageError(error)

    logger.info(f"Artists saved to bucket '{bucket_name}'")


def _publish_to_topic(
    artists: List[Artist],
    queue_topic_arn: str,
    infra_endpoint_url: Optional[str]
):

    queue = boto3.client(
        service_name="sns",
        endpoint_url=infra_endpoint_url
    )

    for artist in artists:

        message = json.dumps({
            "artist": artist.name
        })

        try:
            queue.publish(
                TopicArn=queue_topic_arn,
                Message=message,
            )
        except Exception as error:
            raise PublishMessageError(error)

    logger.info(f"Messages published to topic '{queue_topic_arn}'")


class InvalidKeyType(Exception):
    pass


class MissingEventKey(Exception):
    pass


class MissingEnvVar(Exception):
    pass


class SaveToStorageError(Exception):
    pass


class PublishMessageError(Exception):
    pass
