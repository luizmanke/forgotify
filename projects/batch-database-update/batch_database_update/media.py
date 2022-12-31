from functools import lru_cache
import os
from typing import List

from loguru import logger

from media_tools import Provider
from media_tools import schemas


@lru_cache
def _provider() -> Provider:
    return Provider(
        client_id=os.environ.get("MEDIA_PROVIDER_CLIENT_ID"),
        client_secret=os.environ.get("MEDIA_PROVIDER_CLIENT_SECRET")
    )


def get_artists(queries: List[str]) -> List[schemas.Artist]:

    artists = []
    for query in queries:

        items = _provider().get_artists(query)
        logger.debug(f"Artists for query '{query}' returned {len(items)} items.")

        artists.extend(items)

    return artists


def get_tracks(artists: List[str]) -> List[schemas.Track]:

    tracks = []
    for artist in artists:

        items = _provider().get_tracks(artist)
        logger.debug(f"Tracks for artist '{artist}' returned {len(items)} items.")

        tracks.extend(items)

    return tracks
