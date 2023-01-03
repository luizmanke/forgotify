from typing import List

from fastapi.testclient import TestClient
import pytest

from media_tools.schemas import Playlist

from server.main import app


@pytest.fixture
def client():
    return TestClient(app)


class FakeProvider:

    def __init__(self, n_samples: int):
        self.n_samples = n_samples

    def get_playlists(self, *args, **kwargs) -> List[Playlist]:

        artists = []
        for i in range(self.n_samples):
            artists.append(
                Playlist(
                    id="some-id",
                    name="some-name",
                    description="some-description",
                    url="some-url"
                )
            )

        return artists


def test_get_playlists_with_no_result(mocker, client):

    mocker.patch(
        "server.media._provider",
        return_value=FakeProvider(n_samples=0)
    )

    user_id = "some-user-id"

    response = client.get(f"/playlists/{user_id}")

    assert response.status_code == 200
    assert response.json() == {"playlists": []}


def test_get_playlists_with_some_results(mocker, client):

    mocker.patch(
        "server.media._provider",
        return_value=FakeProvider(n_samples=50)
    )

    user_id = "some-user-id"

    response = client.get(f"/playlists/{user_id}")

    assert response.status_code == 200
    assert response.json() == {
        "playlists": [{
            "id": "some-id",
            "name": "some-name",
            "description": "some-description",
            "url": "some-url"
        }] * 50
    }
