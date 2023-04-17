import os
from typing import Any, Dict

from loguru import logger

from media_tools.search import Provider


def run(event: Dict, context: Any):

    media_client_id = os.environ.get("MEDIA_CLIENT_ID")
    media_client_secret = os.environ.get("MEDIA_CLIENT_SECRET")
    query = event.get("query")

    if not media_client_id:
        raise MissingEnvVar("The 'MEDIA_CLIENT_ID' environment variable is missing")

    if not media_client_secret:
        raise MissingEnvVar("The 'MEDIA_CLIENT_SECRET' environment variable is missing")

    if not query:
        raise MissingEventKey("The 'event' argument is missing the 'query' key")

    if not isinstance(query, str):
        raise InvalidKeyType("The 'event' key 'query' must be of type 'str'")

    media_provider = Provider(media_client_id, media_client_secret)
    artists = media_provider.get_artists(query)
    logger.info(f"Query '{query}' returned {len(artists)} artists")

    # Save to bucket

    return {
        "status_code": 200
    }


class InvalidKeyType(Exception):
    pass


class MissingEventKey(Exception):
    pass


class MissingEnvVar(Exception):
    pass
