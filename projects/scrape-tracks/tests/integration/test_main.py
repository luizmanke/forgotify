from typing import List

import pytest
from freezegun import freeze_time

from database_tools.storage import Bucket

from scrape_tracks import main


class FakeMediaProvider:

    def get_tracks(self, *args, **kwargs) -> List[main.Track]:
        return [
            main.Track(
                id="0",
                name="name",
                popularity=0.0,
                artists_id=["0"]
            )
        ]


@pytest.fixture
def mock_media_provider(mocker):
    mocker.patch(
        "scrape_tracks.main.Provider",
        return_value=FakeMediaProvider()
    )


@pytest.fixture
def bucket():
    return Bucket(
        bucket_name="test-bucket",
        endpoint_url="http://infra:4566"
    )


@freeze_time("2023-01-01")
def test_run_should_save_to_storage(
    mock_media_provider,
    bucket
):
    event = {
        "Records": [{
            "body": '{"artist_id": "0", "artist_name": "A"}'
        }]
    }
    context = {}

    output = main.run(event, context)

    assert output == {"status_code": 200}
    assert bucket.get_json("2023/01/01/0_20230101_000000.json") == [{
        "id": "0",
        "name": "name",
        "popularity": 0.0,
        "artists_id": ["0"]
    }]


def test_run_should_raise_if_event_does_not_contain_records_key():

    event = {}
    context = {}

    with pytest.raises(main.MissingEventKey):
        main.run(event, context)


@pytest.mark.parametrize(
    "body",
    [
        '{"artist_id": "0"}',
        '{"artist_name": "A"}'
    ]
)
def test_run_should_raise_if_event_does_not_contain_key(body):

    event = {
        "Records": [{
            "body": body
        }]
    }
    context = {}

    with pytest.raises(main.MissingEventKey):
        main.run(event, context)


@pytest.mark.parametrize(
    "body",
    [
        '{"artist_id": ["0"], "artist_name": "A"}',
        '{"artist_id": "0", "artist_name": ["A"]}'
    ]
)
def test_run_should_raise_if_key_is_not_string(body):

    event = {
        "Records": [{
            "body": body
        }]
    }
    context = {}

    with pytest.raises(main.InvalidKeyType):
        main.run(event, context)


@pytest.mark.parametrize(
    "env_var",
    [
        "BUCKET_NAME",
        "MEDIA_CLIENT_ID",
        "MEDIA_CLIENT_SECRET"
    ]
)
def test_run_should_raise_if_environment_variable_is_missing(monkeypatch, env_var):

    monkeypatch.delenv(env_var)

    event = {
        "Records": [{
            "body": '{"artist_id": "0", "artist_name": "A"}'
        }]
    }
    context = {}

    with pytest.raises(main.MissingEnvVar):
        main.run(event, context)
