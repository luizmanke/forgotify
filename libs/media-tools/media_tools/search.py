from typing import List

from loguru import logger

from media_tools import schemas
from media_tools import utils


def get_artists(query: str) -> List[schemas.Artist]:

    MAX_ITEMS_PER_REQUEST = 50
    MAX_OFFSET = 1_000
    provider = utils.get_provider()

    offset = 0
    artists = []
    for offset in range(0, MAX_OFFSET, MAX_ITEMS_PER_REQUEST):
        logger.debug(f"Requesting offset {offset}.")

        response = provider.search(query, type="artist", limit=MAX_ITEMS_PER_REQUEST, offset=offset)
        for item in response["artists"]["items"]:
            artists.append(
                schemas.Artist(
                    id=item["id"],
                    name=item["name"],
                    n_followers=item["followers"]["total"],
                    genres=item["genres"],
                    popularity=item["popularity"]
                )
            )

        if len(artists) >= response["artists"]["total"]:
            break

    return artists
