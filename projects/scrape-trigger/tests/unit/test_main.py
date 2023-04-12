import pytest

from scrape_trigger import main


class FakeClient:

    def __init__(self):
        self.published_messages = []

    def publish(self, **kwargs):
        self.published_messages.append(kwargs)


def test_run_publish_messages_and_return_status_200(mocker, monkeypatch):

    fake_client = FakeClient()
    mocker.patch("scrape_trigger.main.boto3.client", return_value=fake_client)

    monkeypatch.setenv("SNS_TOPIC_ARN", "fake-sns-topic-arn")

    event = {"search": ["A"]}
    context = {}

    output = main.run(event, context)

    assert fake_client.published_messages == [{
        "Message": '{"search": "A"}',
        "MessageStructure": "json",
        "TopicArn": "fake-sns-topic-arn",
    }]

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
