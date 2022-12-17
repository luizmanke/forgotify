from datetime import datetime
import string

from batch_database_update import database
from batch_database_update import media


def update_artists() -> None:

    execution_time = datetime.utcnow()

    artists = media.get_artists(list(string.ascii_uppercase))
    database.add_artists(artists, execution_time)


def update_tracks() -> None:

    execution_time = datetime.utcnow()

    artists_name = [artist.name for artist in database.get_artists()]
    tracks = media.get_tracks(artists_name)
    database.add_tracks(tracks, execution_time)
