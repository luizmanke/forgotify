from datetime import datetime
import os
import string

from loguru import logger

from database_tools.postgres import Session
from media_tools.search import Provider

from batch_database_update import models


def _get_and_update_artists(
    media_provider: Provider,
    db_session: Session,
    execution_time: datetime
):

    for query in list(string.ascii_uppercase):
        logger.debug(f"Artist query: '{query}'.")
        artists = media_provider.get_artists(query)

        for artist in artists:
            items = db_session.search(models.Artist, (models.Artist.id == artist.id))

            if not items:
                db_session.add(
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
                db_session.update(item)


def run():

    execution_time = datetime.utcnow()

    media_provider = Provider(
        client_id=os.environ.get("MEDIA_PROVIDER_CLIENT_ID"),
        client_secret=os.environ.get("MEDIA_PROVIDER_CLIENT_SECRET")
    )

    db_session = Session(
        host=os.environ.get("DATABASE_HOST"),
        port=os.environ.get("DATABASE_PORT"),
        username=os.environ.get("DATABASE_USERNAME"),
        password=os.environ.get("DATABASE_PASSWORD"),
        database=os.environ.get("DATABASE_NAME"),
    )

    _get_and_update_artists(media_provider, db_session, execution_time)
