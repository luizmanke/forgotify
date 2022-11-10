from datetime import datetime
from typing import List

from media_tools import schemas
import pytest

from batch_database_update import models
from batch_database_update.main import run
from batch_database_update.main import Session


class FakeProvider:

    def __init__(self, n_samples: int):
        self.n_samples = n_samples

    def get_artists(self, *args, **kwargs) -> List[schemas.Artist]:

        artists = []
        for i in range(self.n_samples):
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
def set_ascii_uppercase_return(monkeypatch):
    monkeypatch.setattr("batch_database_update.main.string.ascii_uppercase", "A")


@pytest.fixture(scope="session")
def db_session():
    return Session(
        host="postgres",
        port="5432",
        username="user",
        password="password",
        database="database",
    )


@pytest.fixture
def clear_table(db_session: Session):
    yield
    db_session._session.query(models.Artist).delete()


@pytest.fixture
def populate_table(db_session: Session, clear_table):
    for item in FakeProvider(n_samples=10).get_artists():
        db_session._session.add(
            models.Artist(
                id=item.id,
                name=item.name,
                n_followers=item.n_followers,
                popularity=item.popularity,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        )
        db_session._session.commit()


@pytest.fixture
def search_with_no_results(mocker):
    mocker.patch(
        "batch_database_update.main.Provider",
        return_value=FakeProvider(n_samples=0)
    )


@pytest.fixture
def search_with_some_results(mocker):
    mocker.patch(
        "batch_database_update.main.Provider",
        return_value=FakeProvider(n_samples=500)
    )


def test_run_with_no_results(
    db_session: Session,
    set_ascii_uppercase_return,
    search_with_no_results
):
    assert db_session.count(models.Artist) == 0
    run()
    assert db_session.count(models.Artist) == 0


def test_run_with_some_results(
    db_session: Session,
    set_ascii_uppercase_return,
    search_with_some_results,
    clear_table
):
    assert db_session.count(models.Artist) == 0
    run()
    assert db_session.count(models.Artist) == 500


def test_run_with_some_results_and_database_has_data(
    db_session: Session,
    populate_table,
    set_ascii_uppercase_return,
    search_with_some_results
):
    assert db_session.count(models.Artist) == 10
    run()
    assert db_session.count(models.Artist) == 500
