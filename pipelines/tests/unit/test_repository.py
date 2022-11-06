from pipelines.repository import main


def test_repository_returns_list():

    response = main()

    assert len(response.get_all_pipelines()) > 0
