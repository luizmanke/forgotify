from datetime import datetime
import os
import pytest

from batch_database_update import main
from batch_database_update import media
from batch_database_update import models
from batch_database_update.database import Session


@pytest.fixture
def set_ascii_uppercase_return(monkeypatch):
    monkeypatch.setattr("batch_database_update.media.string.ascii_uppercase", "A")


@pytest.fixture
def limit_get_artists_items(mocker):
    mocker.patch.object(media.Provider.get_artists, "__defaults__", (50,))


@pytest.fixture(scope="session")
def session() -> Session:
    return Session(
        host=os.environ.get("DATABASE_HOST"),
        port=os.environ.get("DATABASE_PORT"),
        username=os.environ.get("DATABASE_USERNAME"),
        password=os.environ.get("DATABASE_PASSWORD"),
        database=os.environ.get("DATABASE_NAME"),
    )


def test_run(session: Session, set_ascii_uppercase_return, limit_get_artists_items):

    execution_time = datetime.utcnow()

    main.run()

    items_updated = session.search(models.Artist, models.Artist.updated_at > execution_time)
    assert len(items_updated) > 0
