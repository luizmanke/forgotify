import json
import os
import pytest
from typing import List

import boto3

from scrape_trigger import main


class MessageBroker:

    def __init__(self):

        self._sqs = boto3.client(
            service_name="sqs",
            endpoint_url=os.environ["INFRA_ENDPOINT_URL"]
        )

        self._queue = self._sqs.get_queue_url(QueueName="test-queue")

    @property
    def messages(self) -> List:

        response = self._sqs.receive_message(
            QueueUrl=self._queue["QueueUrl"],
            MaxNumberOfMessages=10
        )

        if "Messages" not in response:
            return []

        messages = []
        for item in response["Messages"]:
            body = json.loads(item["Body"])
            messages.append(body["Message"])

        return messages


@pytest.fixture
def message_broker():
    return MessageBroker()


def test_run_should_publish_messages_and_return_status_code_200(message_broker):

    event = {"search": ["A"]}
    context = {}

    output = main.run(event, context)

    assert '{"search": "A"}' in message_broker.messages

    assert output == {
        "status_code": 200,
        "search": ["A"]
    }


def test_run_should_raise_if_event_does_not_contain_search_key():

    event = {}
    context = {}

    with pytest.raises(main.MissingEventKey):
        main.run(event, context)


def test_run_should_raise_if_event_search_key_is_not_list():

    event = {"search": "A"}
    context = {}

    with pytest.raises(main.InvalidKeyType):
        main.run(event, context)


def test_run_should_raise_if_publish_fails(monkeypatch):

    monkeypatch.setenv("SNS_TOPIC_ARN", "wrong-topic-arn")

    event = {"search": ["A"]}
    context = {}

    with pytest.raises(main.PublishError):
        main.run(event, context)
