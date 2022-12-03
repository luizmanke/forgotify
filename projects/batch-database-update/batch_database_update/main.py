from datetime import datetime

from batch_database_update import database
from batch_database_update import media


def _get_and_update_artists(execution_time: datetime) -> None:

    artists = media.get_artists()
    for artist in artists:
        database.add_artist(artist, execution_time)


def run() -> None:

    execution_time = datetime.utcnow()

    _get_and_update_artists(execution_time)
