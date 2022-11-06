from datetime import datetime
import os
import string

from loguru import logger

from database_tools.postgres import Session
from media_tools import search

from batch_database_update import models


def _get_and_update_artists(session: Session, execution_time: datetime):

    for query in list(string.ascii_uppercase):
        logger.debug(f"Artist query: '{query}'.")
        artists = search.get_artists(query)

        for artist in artists:
            items = session.search(models.Artist, (models.Artist.id == artist.id))

            if not items:
                session.add(
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
                session.update(item)


def run():

    execution_time = datetime.utcnow()

    session = Session(
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
        username=os.environ.get("POSTGRES_USERNAME"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        database=os.environ.get("POSTGRES_DATABASE"),
    )

    _get_and_update_artists(session, execution_time)
