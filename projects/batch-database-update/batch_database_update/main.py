from datetime import datetime

from database_tools.postgres import Session
from media_tools import search

from batch_database_update import models


def run():

    execution_time = datetime.utcnow()

    session = Session(
        host="postgres",
        port="5432",
        username="user",
        password="password",
        database="database",
    )

    for query in ["A"]:
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
