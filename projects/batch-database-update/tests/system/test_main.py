from datetime import datetime
import os
import pytest

from batch_database_update import database
from batch_database_update import main
from batch_database_update import media
from batch_database_update import models
from batch_database_update.database import Session


@pytest.fixture
def set_ascii_uppercase_return(monkeypatch):
    monkeypatch.setattr("batch_database_update.main.string.ascii_uppercase", "A")


@pytest.fixture
def limit_media_get_artists_items(mocker):
    mocker.patch.object(media.Provider.get_artists, "__defaults__", (50,))


@pytest.fixture
def limit_media_get_tracks_items(mocker):
    mocker.patch.object(media.Provider.get_tracks, "__defaults__", (50,))


@pytest.fixture
def limit_database_get_artists_items(mocker):
    mocker.patch.object(database.get_artists, "__defaults__", (1,))


@pytest.fixture(scope="session")
def session() -> Session:
    return Session(
        host=os.environ.get("DATABASE_HOST"),
        port=os.environ.get("DATABASE_PORT"),
        username=os.environ.get("DATABASE_USERNAME"),
        password=os.environ.get("DATABASE_PASSWORD"),
        database=os.environ.get("DATABASE_NAME"),
    )


def test_run(
    session,
    set_ascii_uppercase_return,
    limit_media_get_artists_items,
    limit_media_get_tracks_items,
    limit_database_get_artists_items
):

    execution_time = datetime.utcnow()

    main.run()

    artists_updated = session.search(models.Artist, models.Artist.updated_at > execution_time)
    assert len(artists_updated) > 0

    tracks_updated = session.search(models.Track, models.Track.updated_at > execution_time)
    assert len(tracks_updated) > 0
