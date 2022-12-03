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

    def _search(self, query: str, type: str, max_items: int = 1_000) -> List[dict]:

        MAX_ITEMS_PER_REQUEST = 50
        MAX_OFFSET = 1_000
        TYPE_TO_RESPONSE_KEY = {
            "artist": "artists",
            "track": "tracks"
        }

        offset = 0
        items = []
        key = TYPE_TO_RESPONSE_KEY[type]

        for offset in range(0, MAX_OFFSET, MAX_ITEMS_PER_REQUEST):
            logger.debug(f"Requesting offset {offset}.")

            response = self.search(query, type=type, limit=MAX_ITEMS_PER_REQUEST, offset=offset)
            for item in response[key]["items"]:
                items.append(item)

            n_items_is_gte_total_results = len(items) >= response[key]["total"]
            n_items_is_gte_max_items = len(items) >= max_items
            if n_items_is_gte_total_results or n_items_is_gte_max_items:
                break

        return items

    def get_artists(self, query: str, max_items: int = 1_000) -> List[schemas.Artist]:

        artists = []
        for item in self._search(query, "artist", max_items):
            artists.append(
                schemas.Artist(
                    id=item["id"],
                    name=item["name"],
                    n_followers=item["followers"]["total"],
                    genres=item["genres"],
                    popularity=item["popularity"]
                )
            )

        return artists

    def get_tracks(self, artist: str, max_items: int = 1_000) -> List[schemas.Track]:

        tracks = []
        for item in self._search(f"artist:{artist}", "track", max_items):
            tracks.append(
                schemas.Track(
                    id=item["id"],
                    name=item["name"],
                    popularity=item["popularity"],
                    artists_id=[x["id"] for x in item["artists"]],
                )
            )

        return tracks
