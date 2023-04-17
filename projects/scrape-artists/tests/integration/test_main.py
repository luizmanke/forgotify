import pytest

from scrape_artists import main


def test_run_should_save_results_to_bucket_and_return_status_code_200():

    event = {"search": "A"}
    context = {}

    output = main.run(event, context)

    # Assert bucket save

    assert output == {"status_code": 200}


def test_run_should_raise_if_event_does_not_contain_search_key():

    event = {}
    context = {}

    with pytest.raises(main.MissingEventKey):
        main.run(event, context)


def test_run_should_raise_if_event_search_key_is_not_string():

    event = {"search": ["A"]}
    context = {}

    with pytest.raises(main.InvalidKeyType):
        main.run(event, context)
