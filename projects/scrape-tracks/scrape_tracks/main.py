import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from loguru import logger

from database_tools.storage import Bucket
from media_tools.schemas import Track
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

    tracks = _get_tracks(
        artist=event["artist"],
        media_client_id=os.environ["MEDIA_CLIENT_ID"],
        media_client_secret=os.environ["MEDIA_CLIENT_SECRET"]
    )

    _save_to_storage(
        tracks,
        bucket_name=os.environ["BUCKET_NAME"],
        endpoint_url=os.environ.get("INFRA_ENDPOINT_URL")
    )


def _check_inputs(event: Dict):

    bucket_name = os.environ.get("BUCKET_NAME")
    media_client_id = os.environ.get("MEDIA_CLIENT_ID")
    media_client_secret = os.environ.get("MEDIA_CLIENT_SECRET")
    artist = event.get("artist")

    if not bucket_name:
        raise MissingEnvVar("The 'BUCKET_NAME' environment variable is missing")

    if not media_client_id:
        raise MissingEnvVar("The 'MEDIA_CLIENT_ID' environment variable is missing")

    if not media_client_secret:
        raise MissingEnvVar("The 'MEDIA_CLIENT_SECRET' environment variable is missing")

    if not artist:
        raise MissingEventKey("The 'event' argument is missing the 'artist' key")

    if not isinstance(artist, str):
        raise InvalidKeyType("The 'event' key 'artist' must be of type 'str'")


def _get_tracks(
    artist: str,
    media_client_id: str,
    media_client_secret: str
) -> List[Track]:

    media_provider = Provider(
        media_client_id,
        media_client_secret
    )

    tracks = media_provider.get_tracks(artist)
    logger.info(f"Artist '{artist}' returned {len(tracks)} tracks")

    return tracks


def _save_to_storage(
    tracks: List[Track],
    bucket_name: str,
    endpoint_url: Optional[str] = None
):
    current_time = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    bucket = Bucket(
        bucket_name,
        endpoint_url
    )

    for track in tracks:
        bucket.put_json(
            data=track.dict(),
            file_path=f"{current_time}/{track.id}.json"
        )

    logger.info(f"Tracks saved to bucket '{bucket_name}'")


class InvalidKeyType(Exception):
    pass


class MissingEventKey(Exception):
    pass


class MissingEnvVar(Exception):
    pass
