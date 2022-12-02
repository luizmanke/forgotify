from typing import List

from loguru import logger
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from media_tools import schemas


class Credentials(SpotifyClientCredentials):
    pass


class Provider(Spotify):

    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(client_credentials_manager=Credentials(client_id, client_secret))

    def get_artists(self, query: str, max_items: int = 1_000) -> List[schemas.Artist]:

        MAX_ITEMS_PER_REQUEST = 50
        MAX_OFFSET = 1_000

        offset = 0
        artists = []
        for offset in range(0, MAX_OFFSET, MAX_ITEMS_PER_REQUEST):
            logger.debug(f"Requesting offset {offset}.")

            response = self.search(query, type="artist", limit=MAX_ITEMS_PER_REQUEST, offset=offset)
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

            n_items_is_gte_total_results = len(artists) >= response["artists"]["total"]
            n_items_is_gte_max_items = len(artists) >= max_items
            if n_items_is_gte_total_results or n_items_is_gte_max_items:
                break

        return artists
