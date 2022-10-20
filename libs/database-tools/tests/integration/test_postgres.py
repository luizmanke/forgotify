import pytest

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

from database_tools.postgres import ItemIsNotPersistedError
from database_tools.postgres import Session


Base = declarative_base()


class Music(Base):  # type: ignore
    __tablename__ = "musics"

    title = Column(String, primary_key=True)
    author = Column(String)
    year = Column(Integer)


@pytest.fixture
def item():
    return Music(
        title="some-music",
        author="some-author",
        year=2022
    )


@pytest.fixture(scope="session")
def session():
    return Session(
        host="postgres",
        port="5432",
        username="user",
        password="password",
        database="database",
    )


@pytest.fixture(scope="session")
def create_table(session: Session):
    Music.__table__.create(session._engine)


@pytest.fixture
def clear_table(session: Session):
    yield
    session._session.query(Music).delete()


@pytest.fixture
def populate_table(session: Session, create_table, item: Music, clear_table):
    session._session.add(item)
    session._session.commit()


def test_search_with_no_results(session: Session, create_table):
    items = session.search(Music)
    assert len(items) == 0


def test_search_with_results(session: Session, populate_table):
    items = session.search(Music)
    assert len(items) == 1


def test_count_with_no_results(session: Session, create_table):
    assert session.count(Music) == 0


def test_count_with_results(session: Session, populate_table):
    assert session.count(Music) == 1


def test_add_new_item(session: Session, create_table, item: Music, clear_table):
    assert session.count(Music) == 0
    session.add(item)
    assert session.count(Music) == 1


def test_add_item_that_already_exists(session: Session, populate_table, item: Music):
    assert session.count(Music) == 1
    session.add(item)
    assert session.count(Music) == 1


def test_update_item(session: Session, populate_table, item: Music):

    assert session.count(Music) == 1
    assert session.search(Music)[0] == item

    item.year = 2000
    session.update(item)

    assert session.count(Music) == 1
    assert session.search(Music)[0] == item
    assert session.count(Music) == 1


def test_delete_item(session: Session, populate_table, item: Music):
    assert session.count(Music) == 1
    session.delete(item)
    assert session.count(Music) == 0


def test_delete_item_that_does_not_exist(session: Session, create_table, item: Music):
    with pytest.raises(ItemIsNotPersistedError):
        session.delete(item)
