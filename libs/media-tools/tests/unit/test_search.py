import pytest

from media_tools import search


class MockProvider:

    MAX_SAMPLES_PER_SEARCH = 50
    SAMPLE = {
        "id": "some-id",
        "name": "some-name",
        "followers": {"total": 100},
        "genres": ["some-genre"],
        "popularity": 100
    }

    def __init__(self, total_samples):
        self.total_samples = total_samples

    def search(self, *args, **kwargs):
        n_samples = min(self.total_samples, self.MAX_SAMPLES_PER_SEARCH)
        return {
            "artists": {
                "items": [self.SAMPLE] * n_samples,
                "total": self.total_samples
            }
        }


@pytest.fixture
def search_with_no_results(monkeypatch):
    monkeypatch.setattr(
        "media_tools.search.get_provider",
        lambda: MockProvider(total_samples=0)
    )


@pytest.fixture
def search_with_some_results(monkeypatch):
    monkeypatch.setattr(
        "media_tools.search.get_provider",
        lambda: MockProvider(total_samples=500)
    )


@pytest.fixture
def search_with_too_many_results(monkeypatch):
    monkeypatch.setattr(
        "media_tools.search.get_provider",
        lambda: MockProvider(total_samples=10_000)
    )


def test_get_artists_with_no_results(search_with_no_results):
    artists = search.get_artists("some-artist-query")
    assert len(artists) == 0


def test_get_artists_with_some_results(search_with_some_results):
    artists = search.get_artists("some-artist-query")
    assert len(artists) == 500


def test_get_artists_with_too_many_results(search_with_too_many_results):
    artists = search.get_artists("some-artist-query")
    assert len(artists) == 1_000
