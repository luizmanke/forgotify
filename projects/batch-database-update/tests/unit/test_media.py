from typing import List

from media_tools import schemas
import pytest

from batch_database_update import media


class FakeProvider:

    def __init__(self, n_samples: int):
        self.n_samples = n_samples

    def get_artists(self, *args, **kwargs) -> List[schemas.Artist]:

        artists = []
        for i in range(self.n_samples):
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
def set_ascii_uppercase_return(monkeypatch):
    monkeypatch.setattr("batch_database_update.media.string.ascii_uppercase", "ABC")


def test_get_artists_with_no_results(
    mocker,
    set_ascii_uppercase_return
):
    mocker.patch(
        "batch_database_update.media._provider",
        return_value=FakeProvider(n_samples=0)
    )

    artists = media.get_artists()

    assert len(artists) == 0


def test_get_artists_with_some_results(
    mocker,
    set_ascii_uppercase_return
):
    mocker.patch(
        "batch_database_update.media._provider",
        return_value=FakeProvider(n_samples=50)
    )

    artists = media.get_artists()

    assert len(artists) == 150
    assert artists[0] == schemas.Artist(
        id="0",
        name="some-name",
        n_followers=0,
        genres=["some-genre"],
        popularity=0.0
    )
