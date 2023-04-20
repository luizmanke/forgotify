import pytest

from cloud_tools import messenger


@pytest.fixture
def queue():
    return messenger.Queue(
        queue_name="test-queue",
        endpoint_url="http://infra:4566"
    )


def test_queue_should_raise_if_enpoint_url_is_invalid():

    with pytest.raises(messenger.EndpointUrlError):
        messenger.Queue(
            queue_name="test-queue",
            endpoint_url="http://wrong-url:4566"
        )


def test_queue_should_raise_if_queue_name_is_invalid():

    with pytest.raises(messenger.QueueDoesNotExist):
        messenger.Queue(
            queue_name="wrong-queue",
            endpoint_url="http://infra:4566"
        )


def test_add_json_should_add_json_message_to_queue(queue):

    message = {"a": 1}

    queue.add_json(message)

    assert queue.get_json() == {"a": 1}


def test_add_json_should_raise_if_message_is_not_json_serializable(queue):

    message = object

    with pytest.raises(messenger.JSONSerializationError):
        queue.add_json(message)


def test_get_json_should_get_json_message_from_queue(queue):

    message = {"a": 1}
    queue.add_json(message)

    output = queue.get_json()

    assert output == {"a": 1}


def test_get_json_should_raise_if_there_are_no_messages_in_queue(queue):

    with pytest.raises(messenger.NoMessagesInQueue):
        queue.get_json()
