from typing import Dict

import pytest

from media_tools.search import Provider


def fake_search(total_samples: int) -> Dict:

    MAX_SAMPLES_PER_SEARCH = 50
    SAMPLE = {
        "id": "some-id",
        "name": "some-name",
        "followers": {"total": 100},
        "genres": ["some-genre"],
        "popularity": 100
    }

    return {
        "artists": {
            "items": [SAMPLE] * min(total_samples, MAX_SAMPLES_PER_SEARCH),
            "total": total_samples
        }
    }


@pytest.fixture
def provider(mocker) -> Provider:

    mocker.patch("media_tools.search.Credentials")

    return Provider(client_id="", client_secret="")


@pytest.fixture
def search_with_no_results(mocker):
    mocker.patch(
        "media_tools.search.Provider.search",
        return_value=fake_search(total_samples=0)
    )


@pytest.fixture
def search_with_some_results(mocker):
    mocker.patch(
        "media_tools.search.Provider.search",
        return_value=fake_search(total_samples=500)
    )


@pytest.fixture
def search_with_too_many_results(mocker):
    mocker.patch(
        "media_tools.search.Provider.search",
        return_value=fake_search(total_samples=10_000)
    )


def test_get_artists_with_no_results(provider: Provider, search_with_no_results):
    artists = provider.get_artists("some-artist-query")
    assert len(artists) == 0


def test_get_artists_with_some_results(provider: Provider, search_with_some_results):
    artists = provider.get_artists("some-artist-query")
    assert len(artists) == 500


def test_get_artists_with_too_many_results(provider: Provider, search_with_too_many_results):
    artists = provider.get_artists("some-artist-query")
    assert len(artists) == 1_000
