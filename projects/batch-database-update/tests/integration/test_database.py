from copy import deepcopy
from datetime import datetime

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
def populate_table(session: Session):
    session.add(
        models.Artist(
            id="0",
            name="some-name",
            n_followers=0,
            popularity=0.0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    )


@pytest.fixture
def clear_table(session: Session):
    yield
    session._session.query(models.Artist).delete()


@pytest.fixture
def artist():
    return schemas.Artist(
        id="0",
        name="some-name",
        n_followers=0,
        genres=["some-genre"],
        popularity=0.0
    )


def test_add_artist_without_item_in_database(session: Session, artist, clear_table):

    items_before = session.search(models.Artist)
    assert len(items_before) == 0

    execution_time = datetime.utcnow()

    database.add_artist(artist, execution_time)

    items_after = session.search(models.Artist)
    assert len(items_after) == 1
    assert items_after[0].id == "0"
    assert items_after[0].name == "some-name"
    assert items_after[0].n_followers == 0
    assert items_after[0].popularity == 0.0
    assert items_after[0].created_at == execution_time
    assert items_after[0].updated_at == execution_time


def test_add_artist_with_item_in_database(session: Session, artist, populate_table, clear_table):

    items_before = deepcopy(session.search(models.Artist))
    assert len(items_before) == 1

    execution_time = datetime.utcnow()

    database.add_artist(artist, execution_time)

    items_after = session.search(models.Artist)
    assert len(items_after) == 1
    assert items_after[0].id == "0"
    assert items_after[0].name == "some-name"
    assert items_after[0].n_followers == 0
    assert items_after[0].popularity == 0.0
    assert items_after[0].created_at == items_before[0].created_at
    assert items_after[0].updated_at > items_before[0].updated_at
