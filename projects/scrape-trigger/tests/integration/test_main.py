import json
import os
from typing import Dict, List

import boto3
import pytest

from scrape_trigger import main


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
            message = json.loads(body["Message"])
            messages.append(message)

        return messages


@pytest.fixture
def queue():
    return FakeQueue()


def test_run_should_publish_messages(queue):

    event = {"queries": ["A"]}
    context = {}

    output = main.run(event, context)

    assert output == {"status_code": 200}
    assert queue.contains({"query": "A"})


def test_run_should_raise_if_event_does_not_contain_search_key():

    event = {}
    context = {}

    with pytest.raises(main.MissingEventKey):
        main.run(event, context)


def test_run_should_raise_if_event_search_key_is_not_list():

    event = {"queries": "A"}
    context = {}

    with pytest.raises(main.InvalidKeyType):
        main.run(event, context)


@pytest.mark.parametrize(
    "env_var",
    [
        "QUEUE_TOPIC_ARN"
    ]
)
def test_run_should_raise_if_environment_variable_is_missing(monkeypatch, env_var):

    monkeypatch.delenv(env_var)

    event = {"queries": ["A"]}
    context = {}

    with pytest.raises(main.MissingEnvVar):
        main.run(event, context)


def test_run_should_raise_if_publish_message_fails(monkeypatch):

    monkeypatch.setenv("QUEUE_TOPIC_ARN", "wrong-topic-arn")

    event = {"queries": ["A"]}
    context = {}

    with pytest.raises(main.PublishMessageError):
        main.run(event, context)
