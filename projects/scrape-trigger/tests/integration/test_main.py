import pytest

from scrape_trigger import main


def test_run_publish_messages_and_return_status_200():

    event = {"search": ["A"]}
    context = {}

    output = main.run(event, context)

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
