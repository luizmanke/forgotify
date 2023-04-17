import pytest

from scrape_artists import main


class FakeMediaProvider:

    def get_artists(self, *args, **kwargs):
        return []


def test_run_should_save_results_to_bucket_and_return_status_code_200(mocker):

    mocker.patch("scrape_artists.main.Provider", return_value=FakeMediaProvider())

    event = {"query": "A"}
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

    event = {"query": ["A"]}
    context = {}

    with pytest.raises(main.InvalidKeyType):
        main.run(event, context)


@pytest.mark.parametrize(
    "env_var",
    [
        "MEDIA_CLIENT_ID",
        "MEDIA_CLIENT_SECRET"
    ]
)
def test_run_should_raise_if_event_environment_variable_is_missing(monkeypatch, env_var):

    monkeypatch.delenv(env_var)

    event = {"query": "A"}
    context = {}

    with pytest.raises(main.MissingEnvVar):
        main.run(event, context)
