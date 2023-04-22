import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from loguru import logger

from cloud_tools.messenger import Queue
from database_tools.storage import Bucket
from media_tools.schemas import Artist
from media_tools.search import Provider


def run(event: Dict, context: Any) -> Dict:

    if "Records" not in event:
        raise MissingEventKey("The 'event' argument is missing the 'Records' key")

    for record in event["Records"]:
        event = json.loads(record["body"])
        _run(event)

    return {
        "status_code": 200
    }


def _run(event: Dict):

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


def _check_inputs(event: Dict):

    bucket_name = os.environ.get("BUCKET_NAME")
    media_client_id = os.environ.get("MEDIA_CLIENT_ID")
    media_client_secret = os.environ.get("MEDIA_CLIENT_SECRET")
    queue_name = os.environ.get("QUEUE_NAME")
    query = event.get("query")

    if not bucket_name:
        raise MissingEnvVar("The 'BUCKET_NAME' environment variable is missing")

    if not media_client_id:
        raise MissingEnvVar("The 'MEDIA_CLIENT_ID' environment variable is missing")

    if not media_client_secret:
        raise MissingEnvVar("The 'MEDIA_CLIENT_SECRET' environment variable is missing")

    if not queue_name:
        raise MissingEnvVar("The 'QUEUE_NAME' environment variable is missing")

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
    endpoint_url: Optional[str] = None
):
    current_time = datetime.utcnow()
    prefix = current_time.strftime("%Y/%m/%d")
    suffix = current_time.strftime("%Y%m%d_%H%M%S")

    bucket = Bucket(
        bucket_name,
        endpoint_url
    )

    for artist in artists:
        bucket.put_json(
            data=artist.dict(),
            file_path=f"{prefix}/{artist.id}_{suffix}.json"
        )

    logger.info(f"Artists saved to bucket '{bucket_name}'")


def _add_to_queue(
    artists: List[Artist],
    queue_name: str,
    endpoint_url: Optional[str] = None
):
    queue = Queue(
        queue_name,
        endpoint_url
    )

    for artist in artists:
        message = {"artist": artist.name}
        queue.add_json(message)

    logger.info(f"Messages added to queue '{queue_name}'")


class InvalidKeyType(Exception):
    pass


class MissingEventKey(Exception):
    pass


class MissingEnvVar(Exception):
    pass
