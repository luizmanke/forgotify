from datetime import datetime
import string

from batch_database_update import database
from batch_database_update import media


def _get_and_update_artists(execution_time: datetime) -> None:

    artists = media.get_artists(list(string.ascii_uppercase))
    database.add_artists(artists, execution_time)


def _get_and_update_tracks(execution_time: datetime) -> None:

    artists_name = [artist.name for artist in database.get_artists()]
    tracks = media.get_tracks(artists_name)
    database.add_tracks(tracks, execution_time)


def run() -> None:

    execution_time = datetime.utcnow()

    _get_and_update_artists(execution_time)
    _get_and_update_tracks(execution_time)
