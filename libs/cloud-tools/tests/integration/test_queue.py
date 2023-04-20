import pytest

from cloud_tools.queue import Queue


@pytest.fixture
def queue():
    return Queue(
        queue_name="test-queue",
        endpoint_url="http://infra:4566"
    )


def test_add_json_should_add_json_message_to_queue(queue):

    message = {"a": 1}

    queue.add_json(message)

    assert queue.get_json() == {"a": 1}


def test_get_json_should_get_json_message_from_queue(queue):

    message = {"a": 1}
    queue.add_json(message)

    output = queue.get_json()

    assert output == {"a": 1}
