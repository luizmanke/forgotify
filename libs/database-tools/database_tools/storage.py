import json
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


class Bucket:

    def __init__(self, bucket_name: str, endpoint_url: Optional[str] = None):
        self.bucket_name = bucket_name
        self._client = boto3.client(
            service_name="s3",
            endpoint_url=endpoint_url
        )

    def put_json(self, data: Dict, file_path: str):

        if not file_path:
            raise InvalidFilePath(f"Invalid 'file_path': {file_path}")

        try:
            body = json.dumps(data)
        except Exception as error:
            raise JSONSerializationError(error)

        self._client.put_object(
            Body=body,
            Bucket=self.bucket_name,
            Key=file_path
        )

    def get_json(self, file_path: str) -> Dict:

        try:
            item = self._client.get_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
        except ClientError as error:
            if error.response["Error"]["Code"] == "NoSuchKey":
                raise FileDoesntExist(error)
            raise

        content = item["Body"].read()
        return json.loads(content)

    def list_files(self) -> List[str]:

        response = self._client.list_objects(
            Bucket=self.bucket_name
        )

        if "Contents" not in response:
            return []

        return [f["Key"] for f in response["Contents"]]

    def delete_file(self, file_path: str):
        self._client.delete_object(
            Bucket=self.bucket_name,
            Key=file_path
        )


class InvalidFilePath(Exception):
    pass


class JSONSerializationError(Exception):
    pass


class FileDoesntExist(Exception):
    pass
