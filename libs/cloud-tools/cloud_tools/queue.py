import json
from typing import Dict, Optional

import boto3


class Queue:

    def __init__(self, queue_name: str, endpoint_url: Optional[str] = None):

        self._client = boto3.client(
            service_name="sqs",
            endpoint_url=endpoint_url
        )

        self._queue_url = self._client.get_queue_url(QueueName=queue_name)["QueueUrl"]

    def add_json(self, data: Dict):

        message = json.dumps(data)

        self._client.send_message(
            QueueUrl=self._queue_url,
            MessageBody=message,
        )

    def get_json(self) -> Dict:

        response = self._client.receive_message(
            QueueUrl=self._queue_url,
            MaxNumberOfMessages=1
        )

        message = response["Messages"][0]["Body"]
        return json.loads(message)
