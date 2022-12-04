from copy import deepcopy
from datetime import datetime
from typing import List

from media_tools import schemas
import pytest

from batch_database_update import database
from batch_database_update import models
from batch_database_update.database import Session


@pytest.fixture(scope="session")
def session() -> Session:
    return Session(
        host="postgres",
        port="5432",
        username="user",
        password="password",
        database="database",
    )


@pytest.fixture
def populate_artists(session):

    execution_time = datetime.utcnow()

    for i in range(10):
        session.add(
            models.Artist(
                id=f"{i}",
                name="some-name",
                n_followers=0,
                popularity=0.0,
                created_at=execution_time,
                updated_at=execution_time
            )
        )


@pytest.fixture
def populate_tracks(session):

    execution_time = datetime.utcnow()

    for i in range(10):
        session.add(
            models.Track(
                id=f"{i}",
                name="some-name",
                popularity=0.0,
                created_at=execution_time,
                updated_at=execution_time
            )
        )


@pytest.fixture
def populate_artists_to_tracks(session):

    execution_time = datetime.utcnow()

    for artist_id in range(2):
        for track_id in range(10):
            session.add(
                models.ArtistToTrack(
                    artist_id=f"{artist_id}",
                    track_id=f"{track_id}",
                    created_at=execution_time
                )
            )


@pytest.fixture
def clear_table(session):
    yield
    session._session.query(models.Artist).delete()
    session._session.query(models.ArtistToTrack).delete()
    session._session.query(models.Track).delete()


@pytest.fixture
def fake_artists() -> List[schemas.Artist]:

    artists = []
    for i in range(10):
        artists.append(
            schemas.Artist(
                id=f"{i}",
                name="some-name",
                n_followers=0,
                genres=["some-genre"],
                popularity=0.0
            )
        )

    return artists


@pytest.fixture
def fake_tracks() -> List[schemas.Track]:

    tracks = []
    for i in range(10):
        tracks.append(
            schemas.Track(
                id=f"{i}",
                name="some-name",
                popularity=0.0,
                artists_id=["0", "1"]
            )
        )

    return tracks


def test_add_artists_without_item_in_database(session, fake_artists, clear_table):

    artists_before = session.search(models.Artist)
    assert len(artists_before) == 0

    execution_time = datetime.utcnow()

    database.add_artists(fake_artists, execution_time)

    artists_after = session.search(models.Artist)
    assert len(artists_after) == 10
    assert artists_after[0].id == "0"
    assert artists_after[0].name == "some-name"
    assert artists_after[0].n_followers == 0
    assert artists_after[0].popularity == 0.0
    assert artists_after[0].created_at == execution_time
    assert artists_after[0].updated_at == execution_time


def test_add_artists_with_item_in_database(session, fake_artists, populate_artists, clear_table):

    artists_before = deepcopy(session.search(models.Artist))
    assert len(artists_before) == 10

    execution_time = datetime.utcnow()

    database.add_artists(fake_artists, execution_time)

    artists_after = session.search(models.Artist)
    assert len(artists_after) == 10
    assert artists_after[0].id == "0"
    assert artists_after[0].name == "some-name"
    assert artists_after[0].n_followers == 0
    assert artists_after[0].popularity == 0.0
    assert artists_after[0].created_at == artists_before[0].created_at
    assert artists_after[0].updated_at > artists_before[0].updated_at


def test_add_tracks_without_item_in_database(session, fake_tracks, clear_table):

    tracks_before = session.search(models.Track)
    assert len(tracks_before) == 0

    artists_to_tracks_before = session.search(models.ArtistToTrack)
    assert len(artists_to_tracks_before) == 0

    execution_time = datetime.utcnow()

    database.add_tracks(fake_tracks, execution_time)

    tracks_after = session.search(models.Track)
    assert len(tracks_after) == 10
    assert tracks_after[0].id == "0"
    assert tracks_after[0].name == "some-name"
    assert tracks_after[0].popularity == 0.0
    assert tracks_after[0].created_at == execution_time
    assert tracks_after[0].updated_at == execution_time

    artists_to_tracks_after = session.search(models.ArtistToTrack)
    assert len(artists_to_tracks_after) == 20
    assert artists_to_tracks_after[0].artist_id == "0"
    assert artists_to_tracks_after[0].track_id == "0"
    assert artists_to_tracks_after[0].created_at == execution_time


def test_add_tracks_with_item_in_database(
    session,
    fake_tracks,
    populate_tracks,
    populate_artists_to_tracks,
    clear_table
):

    tracks_before = deepcopy(session.search(models.Track))
    assert len(tracks_before) == 10

    artists_to_tracks_before = deepcopy(session.search(models.ArtistToTrack))
    assert len(artists_to_tracks_before) == 20

    execution_time = datetime.utcnow()

    database.add_tracks(fake_tracks, execution_time)

    tracks_after = session.search(models.Track)
    assert len(tracks_after) == 10
    assert tracks_after[0].id == "0"
    assert tracks_after[0].name == "some-name"
    assert tracks_after[0].popularity == 0.0
    assert tracks_after[0].created_at == tracks_before[0].created_at
    assert tracks_after[0].updated_at > tracks_before[0].updated_at

    artists_to_tracks_after = session.search(models.ArtistToTrack)
    assert len(artists_to_tracks_after) == 20
