import pytest

from database_tools import storage


@pytest.fixture
def bucket():

    bucket = storage.Bucket(
        bucket_name="test-bucket",
        endpoint_url="http://storage:4566"
    )

    yield bucket

    # Clear bucket
    for file_path in bucket.list_files():
        bucket.delete_file(file_path)


@pytest.mark.parametrize(
    "file_path",
    [
        "file.json",
        "some/dir/file.json"
    ]
)
def test_put_json_should_create_json_file_in_bucket(bucket, file_path):

    data = {"a": 1}

    bucket.put_json(data, file_path)

    assert bucket.get_json(file_path) == {"a": 1}


def test_put_json_should_raise_if_data_is_not_json_serializable(bucket):

    data = object
    file_path = "file.json"

    with pytest.raises(storage.JSONSerializationError):
        bucket.put_json(data, file_path)


def test_put_json_should_raise_if_file_path_is_empty(bucket):

    data = {"a": 1}
    file_path = ""

    with pytest.raises(storage.InvalidFilePath):
        bucket.put_json(data, file_path)


def test_get_json_should_read_json_file_from_bucket(bucket):

    data = {"a": 1}
    file_path = "file.json"
    bucket.put_json(data, file_path)

    output = bucket.get_json(file_path)

    assert output == {"a": 1}


def test_get_json_should_raise_if_path_does_not_exist(bucket):

    file_path = "file.json"

    with pytest.raises(storage.FileDoesntExist):
        bucket.get_json(file_path)


def test_list_files_should_return_the_files_in_bucket(bucket):

    data = {"a": 1}
    file_path = "file.json"
    bucket.put_json(data, file_path)

    files = bucket.list_files()

    assert files == ["file.json"]


def test_delete_file_should_delete_the_file_from_bucket(bucket):

    data = {"a": 1}
    file_path = "file.json"
    bucket.put_json(data, file_path)

    bucket.delete_file(file_path)

    assert bucket.list_files() == []
