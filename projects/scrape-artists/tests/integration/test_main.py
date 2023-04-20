import json
import os
from typing import Dict, List

import boto3
import pytest
from freezegun import freeze_time

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


class FakeQueue:

    def __init__(self):

        self._sqs = boto3.client(
            service_name="sqs",
            endpoint_url=os.environ["INFRA_ENDPOINT_URL"]
        )

        self._queue = self._sqs.get_queue_url(QueueName="test-queue")

    def contains(self, message: Dict) -> bool:
        return message in self.messages

    @property
    def messages(self) -> List:

        response = self._sqs.receive_message(
            QueueUrl=self._queue["QueueUrl"],
            MaxNumberOfMessages=10
        )

        messages = []
        for item in response["Messages"]:
            body = json.loads(item["Body"])
            messages.append(body)

        return messages


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
    return FakeQueue()


@freeze_time("2023-01-01")
def test_run_should_save_to_storage_and_add_to_queue(
    mock_media_provider,
    bucket,
    queue
):

    event = {"query": "A"}
    context = {}

    output = main.run(event, context)

    assert output == {"status_code": 200}
    assert queue.contains({"artist": "name"})
    assert bucket.get_json("20230101_000000/0.json") == {
        "id": "0",
        "name": "name",
        "n_followers": 0,
        "genres": ["genre"],
        "popularity": 0.0
    }


def test_run_should_raise_if_event_does_not_contain_search_key():

    event = {}
    context = {}

    with pytest.raises(main.exceptions.MissingEventKey):
        main.run(event, context)


def test_run_should_raise_if_event_search_key_is_not_string():

    event = {"query": ["A"]}
    context = {}

    with pytest.raises(main.exceptions.InvalidKeyType):
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

    event = {"query": "A"}
    context = {}

    with pytest.raises(main.exceptions.MissingEnvVar):
        main.run(event, context)


def test_run_should_raise_if_get_artists_fails():

    event = {"query": "A"}
    context = {}

    with pytest.raises(main.exceptions.GetArtistsError):
        main.run(event, context)


def test_run_should_raise_if_save_to_storage_fails(
    mock_media_provider,
    monkeypatch
):

    monkeypatch.setenv("BUCKET_NAME", "wrong-bucket-name")

    event = {"query": "A"}
    context = {}

    with pytest.raises(main.exceptions.SaveToStorageError):
        main.run(event, context)


def test_run_should_raise_if_add_to_queue_fails(
    mock_media_provider,
    monkeypatch
):

    monkeypatch.setenv("QUEUE_NAME", "wrong-queue-name")

    event = {"query": "A"}
    context = {}

    with pytest.raises(main.exceptions.AddToQueueError):
        main.run(event, context)
