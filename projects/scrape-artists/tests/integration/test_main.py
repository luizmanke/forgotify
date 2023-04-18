import json
import os
from typing import Dict, List

import boto3
import pytest
from freezegun import freeze_time

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


class FakeStorage:

    def __init__(self):
        self._storage = boto3.client(
            service_name="s3",
            endpoint_url=os.environ["INFRA_ENDPOINT_URL"]
        )

    def get(self, file: str) -> Dict:
        item = self._storage.get_object(
            Bucket=os.environ["BUCKET_NAME"],
            Key=file
        )
        content = item["Body"].read()
        return json.loads(content)


@pytest.fixture
def mock_media_provider(mocker):
    mocker.patch(
        "scrape_artists.main.Provider",
        return_value=FakeMediaProvider()
    )


@pytest.fixture
def storage():
    return FakeStorage()


@freeze_time("2023-01-01")
def test_run_should_save_results_to_bucket_and_return_status_code_200(
    mock_media_provider,
    storage
):

    event = {"query": "A"}
    context = {}

    output = main.run(event, context)

    assert output == {"status_code": 200}
    assert storage.get(file="0_20230101_000000.json") == {
        "id": "0",
        "name": "name",
        "n_followers": 0,
        "genres": ["genre"],
        "popularity": 0.0
    }


def test_run_should_raise_if_event_does_not_contain_search_key():

    event = {}
    context = {}

    with pytest.raises(main.MissingEventKey):
        main.run(event, context)


def test_run_should_raise_if_event_search_key_is_not_string():

    event = {"query": ["A"]}
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

    event = {"query": "A"}
    context = {}

    with pytest.raises(main.MissingEnvVar):
        main.run(event, context)


def test_run_should_raise_if_save_to_storage_fails(
    mock_media_provider,
    monkeypatch
):

    monkeypatch.setenv("BUCKET_NAME", "wrong-bucket-name")

    event = {"query": "A"}
    context = {}

    with pytest.raises(main.SaveToStorageError):
        main.run(event, context)
