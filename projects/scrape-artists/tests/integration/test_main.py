from typing import List

import pytest
from freezegun import freeze_time

from cloud_tools.messenger import Queue
from database_tools.storage import Bucket

from scrape_artists import main


class FakeMediaProvider:

    def get_artists(self, *args, **kwargs) -> List[main.Artist]:
        return [
            main.Artist(
                id="0",
                name="name",
                n_followers=0,
                genres=["genre"],
                popularity=0.0
            )
        ]


@pytest.fixture
def mock_media_provider(mocker):
    mocker.patch(
        "scrape_artists.main.Provider",
        return_value=FakeMediaProvider()
    )


@pytest.fixture
def bucket():
    return Bucket(
        bucket_name="test-bucket",
        endpoint_url="http://infra:4566"
    )


@pytest.fixture
def queue():
    return Queue(
        queue_name="test-queue",
        endpoint_url="http://infra:4566"
    )


@freeze_time("2023-01-01")
def test_run_should_save_to_storage_and_add_to_queue(
    mock_media_provider,
    bucket,
    queue
):
    event = {
        "Records": [{
            "body": '{"query": "A"}'
        }]
    }
    context = {}

    output = main.run(event, context)

    assert output == {"status_code": 200}
    assert queue.get_json() == {
        "artist_id": "0",
        "artist_name": "name"
    }
    assert bucket.get_json("2023/01/01/0_20230101_000000.json") == {
        "id": "0",
        "name": "name",
        "n_followers": 0,
        "genres": ["genre"],
        "popularity": 0.0
    }


def test_run_should_raise_if_event_does_not_contain_records_key():

    event = {}
    context = {}

    with pytest.raises(main.MissingEventKey):
        main.run(event, context)


def test_run_should_raise_if_event_does_not_contain_query_key():

    event = {
        "Records": [{
            "body": '{}'
        }]
    }
    context = {}

    with pytest.raises(main.MissingEventKey):
        main.run(event, context)


def test_run_should_raise_if_query_key_is_not_string():

    event = {
        "Records": [{
            "body": '{"query": ["A"]}'
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
        "MEDIA_CLIENT_SECRET",
        "QUEUE_NAME"
    ]
)
def test_run_should_raise_if_environment_variable_is_missing(monkeypatch, env_var):

    monkeypatch.delenv(env_var)

    event = {
        "Records": [{
            "body": '{"query": "A"}'
        }]
    }
    context = {}

    with pytest.raises(main.MissingEnvVar):
        main.run(event, context)
