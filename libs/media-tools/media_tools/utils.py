from functools import lru_cache
import os

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class Credentials(SpotifyClientCredentials):
    pass


class Provider(Spotify):

    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(client_credentials_manager=Credentials(client_id, client_secret))


@lru_cache
def get_provider() -> Provider:
    return Provider(
        os.environ.get("MEDIA_TOOLS_CLIENT_ID", ""),
        os.environ.get("MEDIA_TOOLS_CLIENT_SECRET", "")
    )
