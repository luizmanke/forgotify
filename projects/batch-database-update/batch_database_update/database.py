from datetime import datetime
from functools import lru_cache
import os

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


def add_artist(artist: schemas.Artist, execution_time: datetime) -> None:

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
        item.name = artist.name
        item.n_followers = artist.n_followers
        item.popularity = artist.popularity
        item.updated_at = execution_time
        _session().update(item)
