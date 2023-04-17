from typing import Dict


class InvalidKeyType(Exception):
    pass


class MissingEventKey(Exception):
    pass


class PublishError(Exception):
    pass


def run(event, context):

    _validate_input(event)

    # Search artists

    # Save to bucket

    return {
        "status_code": 200
    }


def _validate_input(event: Dict):

    search = event.get("search")

    if not search:
        raise MissingEventKey("The 'event' argument is missing the 'search' key")

    if not isinstance(search, str):
        raise InvalidKeyType("The 'event' key 'search' must be of type 'str'")
