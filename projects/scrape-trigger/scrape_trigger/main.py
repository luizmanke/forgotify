from typing import List


class MissingEventKey(Exception):
    pass


class InvalidKeyType(Exception):
    pass


def run(event, context):

    search = event.get("search")

    if not search:
        raise MissingEventKey("The 'event' argument is missing the 'search' key")

    if not isinstance(search, List):
        raise InvalidKeyType("The 'event' key 'search' must be of type list")

    return {
        "status_code": 200,
        "search": search
    }
