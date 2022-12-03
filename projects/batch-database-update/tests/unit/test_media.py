from typing import List

from media_tools import schemas

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

    def get_tracks(self, *args, **kwargs) -> List[schemas.Track]:

        tracks = []
        for i in range(self.n_samples):
            tracks.append(
                schemas.Track(
                    id=f"{i}",
                    name="some-name",
                    popularity=0.0,
                    artists_id=["some-artist-id"]
                )
            )

        return tracks


def test_get_artists_with_no_results(mocker):

    mocker.patch(
        "batch_database_update.media._provider",
        return_value=FakeProvider(n_samples=0)
    )

    artists = media.get_artists(queries=["A"])

    assert len(artists) == 0


def test_get_artists_with_some_results(mocker):

    mocker.patch(
        "batch_database_update.media._provider",
        return_value=FakeProvider(n_samples=50)
    )

    artists = media.get_artists(queries=["A", "B", "C"])

    assert len(artists) == 150
    assert artists[0] == schemas.Artist(
        id="0",
        name="some-name",
        n_followers=0,
        genres=["some-genre"],
        popularity=0.0
    )


def test_get_tracks_with_no_results(mocker):

    mocker.patch(
        "batch_database_update.media._provider",
        return_value=FakeProvider(n_samples=0)
    )

    tracks = media.get_tracks(artists=["A"])

    assert len(tracks) == 0


def test_get_tracks_with_some_results(mocker):

    mocker.patch(
        "batch_database_update.media._provider",
        return_value=FakeProvider(n_samples=50)
    )

    tracks = media.get_tracks(artists=["A", "B", "C"])

    assert len(tracks) == 150
    assert tracks[0] == schemas.Track(
        id="0",
        name="some-name",
        popularity=0.0,
        artists_id=["some-artist-id"]
    )
