import json
from typing import Dict, Optional

import boto3
from botocore import exceptions


class Queue:

    def __init__(self, queue_name: str, endpoint_url: Optional[str] = None):

        self.queue_name = queue_name

        self._client = boto3.client(
            service_name="sqs",
            endpoint_url=endpoint_url
        )

        try:
            self._queue_url = self._client.get_queue_url(
                QueueName=queue_name
            )["QueueUrl"]
        except exceptions.EndpointConnectionError as e:
            raise EndpointUrlError(e)
        except Exception as e:
            raise QueueDoesNotExist(e)

    def add_json(self, message: Dict):

        try:
            body = json.dumps(message)
        except Exception as e:
            raise JSONSerializationError(e)

        self._client.send_message(
            QueueUrl=self._queue_url,
            MessageBody=body,
        )

    def get_json(self) -> Dict:

        response = self._client.receive_message(
            QueueUrl=self._queue_url,
            MaxNumberOfMessages=1
        )

        if "Messages" not in response:
            raise NoMessagesInQueue(f"There are no messages in queue '{self.queue_name}'")

        message = response["Messages"][0]["Body"]
        return json.loads(message)


class EndpointUrlError(Exception):
    pass


class JSONSerializationError(Exception):
    pass


class NoMessagesInQueue(Exception):
    pass


class QueueDoesNotExist(Exception):
    pass
