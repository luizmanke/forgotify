from functools import lru_cache
from os import environ
from typing import Dict, List

from media_tools import Provider


@lru_cache
def _provider() -> Provider:
    return Provider(
        client_id=environ.get("MEDIA_PROVIDER_CLIENT_ID"),
        client_secret=environ.get("MEDIA_PROVIDER_CLIENT_SECRET")
    )


def get_playlists(user_id: str) -> List[Dict]:
    return [p.dict() for p in _provider().get_playlists(user_id)]
