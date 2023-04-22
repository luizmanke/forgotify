import pytest

from cloud_tools.messenger import Queue

from scrape_trigger import main


@pytest.fixture
def queue():
    return Queue(
        queue_name="test-queue",
        endpoint_url="http://infra:4566"
    )


def test_run_should_add_to_queue(queue):

    event = {"queries": ["A"]}
    context = {}

    output = main.run(event, context)

    assert output == {"status_code": 200}
    assert queue.get_json() == {"query": "A"}


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
        "QUEUE_NAME"
    ]
)
def test_run_should_raise_if_environment_variable_is_missing(monkeypatch, env_var):

    monkeypatch.delenv(env_var)

    event = {"queries": ["A"]}
    context = {}

    with pytest.raises(main.MissingEnvVar):
        main.run(event, context)
