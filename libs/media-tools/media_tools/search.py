from typing import Callable, Dict, List

import backoff
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from media_tools.schemas import Artist, Playlist, Track


class Credentials(SpotifyClientCredentials):
    pass


class Provider(Spotify):

    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(client_credentials_manager=Credentials(client_id, client_secret))

    def get_artists(self, query: str, max_items: int = 1_000) -> List[Artist]:

        artists = []
        for item in self._search_loop(query, "artist", max_items):
            artists.append(
                Artist(
                    id=item["id"],
                    name=item["name"],
                    n_followers=item["followers"]["total"],
                    genres=item["genres"],
                    popularity=item["popularity"]
                )
            )

        return artists

    def get_tracks(self, artist: str, max_items: int = 1_000) -> List[Track]:

        tracks = []
        for item in self._search_loop(f"artist:{artist}", "track", max_items):
            tracks.append(
                Track(
                    id=item["id"],
                    name=item["name"],
                    popularity=item["popularity"],
                    artists_id=[x["id"] for x in item["artists"]],
                )
            )

        return tracks

    def get_playlists(self, user_id: str, max_items: int = 1_000) -> List[Playlist]:

        playlists = []
        for item in self._playlists_loop(user_id, max_items):
            playlists.append(
                Playlist(
                    id=item["id"],
                    name=item["name"],
                    description=item["description"],
                    url=item["external_urls"]["spotify"],
                )
            )

        return playlists

    def _search_loop(self, query: str, type: str, max_items: int) -> List[dict]:

        TYPE_TO_RESPONSE_KEY = {
            "artist": "artists",
            "track": "tracks"
        }

        key = TYPE_TO_RESPONSE_KEY[type]

        def request_function(max_items: int, offset: int) -> Dict:
            response = self._search(query, type, max_items, offset)
            return response[key]

        return self._request_loop(request_function, max_items)

    def _playlists_loop(self, user_id: str, max_items: int) -> List[dict]:

        def request_function(max_items: int, offset: int) -> Dict:
            return self._user_playlists(user_id, max_items, offset)

        return self._request_loop(request_function, max_items)

    def _request_loop(self, request_function: Callable, max_items: int) -> List[dict]:

        MAX_ITEMS_PER_REQUEST = 50
        MAX_OFFSET = 1_000

        offset = 0
        items = []
        for offset in range(0, MAX_OFFSET, MAX_ITEMS_PER_REQUEST):

            response = request_function(MAX_ITEMS_PER_REQUEST, offset)
            for item in response["items"]:
                items.append(item)

            n_items_is_gte_total_results = len(items) >= response["total"]
            n_items_is_gte_max_items = len(items) >= max_items
            if n_items_is_gte_total_results or n_items_is_gte_max_items:
                break

        items_not_none = [item for item in items if item is not None]
        return items_not_none

    @backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError)
    def _search(self, query: str, type: str, max_items: int, offset: int) -> Dict:
        return self.search(query, type=type, limit=max_items, offset=offset)

    @backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError)
    def _user_playlists(self, user_id: str, max_items: int, offset: int) -> Dict:
        return self.user_playlists(user_id, max_items, offset)
