from functools import lru_cache
import os
import string
from typing import List

from loguru import logger

from media_tools.schemas import Artist
from media_tools.search import Provider


@lru_cache
def _provider() -> Provider:
    return Provider(
        client_id=os.environ.get("MEDIA_PROVIDER_CLIENT_ID"),
        client_secret=os.environ.get("MEDIA_PROVIDER_CLIENT_SECRET")
    )


def get_artists() -> List[Artist]:

    artists = []
    for query in list(string.ascii_uppercase):

        items = _provider().get_artists(query)
        logger.debug(f"Artist query '{query}' returned {len(items)} items.")

        artists.extend(items)

    return artists
