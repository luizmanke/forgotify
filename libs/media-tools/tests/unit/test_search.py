from typing import Dict

import pytest

from media_tools import schemas
from media_tools.search import Provider


def fake_artists_search(total_samples: int) -> Dict:

    MAX_SAMPLES_PER_SEARCH = 50
    SAMPLE = {
        "id": "some-id",
        "name": "some-name",
        "followers": {"total": 100},
        "genres": ["some-genre"],
        "popularity": 100.0
    }

    return {
        "artists": {
            "items": [SAMPLE] * min(total_samples, MAX_SAMPLES_PER_SEARCH),
            "total": total_samples
        }
    }


def fake_tracks_search(total_samples: int) -> Dict:

    MAX_SAMPLES_PER_SEARCH = 50
    SAMPLE = {
        "id": "some-id",
        "name": "some-name",
        "popularity": 100.0,
        "artists": [{"id": "some-artist-id"}]
    }

    return {
        "tracks": {
            "items": [SAMPLE] * min(total_samples, MAX_SAMPLES_PER_SEARCH),
            "total": total_samples
        }
    }


@pytest.fixture
def provider(mocker) -> Provider:

    mocker.patch("media_tools.search.Credentials")

    return Provider(client_id="", client_secret="")


def test_get_artists_with_no_results(mocker, provider):

    mocker.patch(
        "media_tools.search.Provider.search",
        return_value=fake_artists_search(total_samples=0)
    )

    artists = provider.get_artists("some-artist-query")

    assert len(artists) == 0


def test_get_artists_with_some_results(mocker, provider):

    mocker.patch(
        "media_tools.search.Provider.search",
        return_value=fake_artists_search(total_samples=500)
    )

    artists = provider.get_artists("some-artist-query")

    assert len(artists) == 500
    assert artists[0] == schemas.Artist(
        id="some-id",
        name="some-name",
        n_followers=100,
        genres=["some-genre"],
        popularity=100.0
    )


def test_get_artists_with_too_many_results(mocker, provider):

    mocker.patch(
        "media_tools.search.Provider.search",
        return_value=fake_artists_search(total_samples=10_000)
    )

    artists = provider.get_artists("some-artist-query")

    assert len(artists) == 1_000
    assert artists[0] == schemas.Artist(
        id="some-id",
        name="some-name",
        n_followers=100,
        genres=["some-genre"],
        popularity=100.0
    )


def test_get_tracks_with_no_results(mocker, provider):

    mocker.patch(
        "media_tools.search.Provider.search",
        return_value=fake_tracks_search(total_samples=0)
    )

    tracks = provider.get_tracks("some-track-query")

    assert len(tracks) == 0


def test_get_tracks_with_some_results(mocker, provider):

    mocker.patch(
        "media_tools.search.Provider.search",
        return_value=fake_tracks_search(total_samples=500)
    )

    tracks = provider.get_tracks("some-track-query")

    assert len(tracks) == 500
    assert tracks[0] == schemas.Track(
        id="some-id",
        name="some-name",
        popularity=100.0,
        artists_id=["some-artist-id"]
    )


def test_get_tracks_with_too_many_results(mocker, provider):

    mocker.patch(
        "media_tools.search.Provider.search",
        return_value=fake_tracks_search(total_samples=10_000)
    )

    tracks = provider.get_tracks("some-track-query")

    assert len(tracks) == 1_000
    assert tracks[0] == schemas.Track(
        id="some-id",
        name="some-name",
        popularity=100.0,
        artists_id=["some-artist-id"]
    )
