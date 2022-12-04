from datetime import datetime
from functools import lru_cache
import os
from typing import List, Optional

from database_tools.postgres import Session
from media_tools import schemas

from batch_database_update import models


@lru_cache
def _session() -> Session:
    return Session(
        host=os.environ.get("DATABASE_HOST"),
        port=os.environ.get("DATABASE_PORT"),
        username=os.environ.get("DATABASE_USERNAME"),
        password=os.environ.get("DATABASE_PASSWORD"),
        database=os.environ.get("DATABASE_NAME"),
    )


def add_artists(artists: List[schemas.Artist], execution_time: datetime) -> None:

    for artist in artists:
        items = _session().search(models.Artist, (models.Artist.id == artist.id))

        if not items:
            _session().add(
                models.Artist(
                    id=artist.id,
                    name=artist.name,
                    n_followers=artist.n_followers,
                    popularity=artist.popularity,
                    created_at=execution_time,
                    updated_at=execution_time
                )
            )

        else:
            item = items[0]
            item.n_followers = artist.n_followers
            item.popularity = artist.popularity
            item.updated_at = execution_time
            _session().update(item)


def add_tracks(tracks: List[schemas.Track], execution_time: datetime) -> None:

    for track in tracks:
        items = _session().search(models.Track, (models.Track.id == track.id))

        if not items:
            _session().add(
                models.Track(
                    id=track.id,
                    name=track.name,
                    popularity=track.popularity,
                    created_at=execution_time,
                    updated_at=execution_time
                )
            )

            for artist_id in track.artists_id:
                _session().add(
                    models.ArtistToTrack(
                        artist_id=artist_id,
                        track_id=track.id,
                        created_at=execution_time,
                    )
                )

        else:
            item = items[0]
            item.popularity = track.popularity
            item.updated_at = execution_time
            _session().update(item)


def get_artists(max_items: Optional[int] = None) -> List[models.Artist]:

    artists = _session().search(models.Artist)
    if max_items:
        artists = artists[:max_items]

    return artists
