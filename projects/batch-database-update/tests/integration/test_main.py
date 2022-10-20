from datetime import datetime
from typing import List

from media_tools import schemas
import pytest

from batch_database_update import models
from batch_database_update.main import run
from batch_database_update.main import Session


@pytest.fixture
def set_ascii_uppercase_return(monkeypatch):
    monkeypatch.setattr("batch_database_update.main.string.ascii_uppercase", "A")


@pytest.fixture(scope="session")
def session():
    return Session(
        host="postgres",
        port="5432",
        username="user",
        password="password",
        database="database",
    )


def create_get_artists_results(n_samples: int) -> List[schemas.Artist]:
    artists = []
    for i in range(n_samples):
        artists.append(
            schemas.Artist(
                id=f"{i}",
                name="",
                n_followers=0,
                genres=[],
                popularity=0.0
            )
        )

    return artists


@pytest.fixture
def clear_table(session: Session):
    yield
    session._session.query(models.Artist).delete()


@pytest.fixture
def populate_table(session: Session, clear_table):
    for item in create_get_artists_results(n_samples=10):
        session._session.add(
            models.Artist(
                id=item.id,
                name=item.name,
                n_followers=item.n_followers,
                popularity=item.popularity,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        )
        session._session.commit()


@pytest.fixture
def search_with_no_results(monkeypatch):
    monkeypatch.setattr(
        "batch_database_update.main.search.get_artists",
        lambda *args, **kwargs: create_get_artists_results(n_samples=0)
    )


@pytest.fixture
def search_with_some_results(monkeypatch):
    monkeypatch.setattr(
        "batch_database_update.main.search.get_artists",
        lambda *args, **kwargs: create_get_artists_results(n_samples=500)
    )


def test_run_with_no_results(
    session,
    set_ascii_uppercase_return,
    search_with_no_results
):
    assert session.count(models.Artist) == 0
    run()
    assert session.count(models.Artist) == 0


def test_run_with_some_results(
    session,
    set_ascii_uppercase_return,
    search_with_some_results,
    clear_table
):
    assert session.count(models.Artist) == 0
    run()
    assert session.count(models.Artist) == 500


def test_run_with_some_results_and_database_has_data(
    session,
    populate_table,
    set_ascii_uppercase_return,
    search_with_some_results
):
    assert session.count(models.Artist) == 10
    run()
    assert session.count(models.Artist) == 500
