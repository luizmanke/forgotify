from pipelines.repository import pipelines


def test_repository_returns_list():

    response = pipelines()

    assert len(response.get_all_pipelines()) > 0
