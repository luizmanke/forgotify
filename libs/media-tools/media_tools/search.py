from typing import List

from loguru import logger
from pydantic import BaseModel

from media_tools.utils import get_provider


class Artist(BaseModel):
    id: str
    name: str
    followers: int
    genres: list
    popularity: float


def get_artists(query: str) -> List[Artist]:

    MAX_ITEMS_PER_REQUEST = 50
    MAX_OFFSET = 1_000
    provider = get_provider()

    offset = 0
    artists = []
    while True:
        logger.debug(f"Requesting offset {offset}.")

        response = provider.search(query, type="artist", limit=MAX_ITEMS_PER_REQUEST, offset=offset)
        for item in response["artists"]["items"]:
            artists.append(Artist(
                id=item["id"],
                name=item["name"],
                followers=item["followers"]["total"],
                genres=item["genres"],
                popularity=item["popularity"]
            ))

        offset += MAX_ITEMS_PER_REQUEST
        if offset >= min(response["artists"]["total"], MAX_OFFSET):
            break

    return artists
