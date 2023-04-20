import pytest

from cloud_tools.queue import Queue


@pytest.fixture
def queue():
    return Queue()


def test_publish_should_add_message_to_queue(queue):

    message = {"a": 1}

    queue.publish(message)

    assert message in queue.list()
