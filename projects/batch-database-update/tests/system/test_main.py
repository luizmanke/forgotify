import pytest

from batch_database_update import main


@pytest.fixture
def set_ascii_uppercase_return(monkeypatch):
    monkeypatch.setattr("batch_database_update.main.string.ascii_uppercase", "A")


@pytest.fixture
def limit_get_artists_items(mocker):
    mocker.patch.object(main.Provider.get_artists, "__defaults__", (50,))


def test_run(set_ascii_uppercase_return, limit_get_artists_items):

    main.run()
