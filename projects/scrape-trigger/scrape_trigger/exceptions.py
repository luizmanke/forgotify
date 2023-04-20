class InvalidKeyType(Exception):
    pass


class MissingEventKey(Exception):
    pass


class MissingEnvVar(Exception):
    pass


class AddToQueueError(Exception):
    pass


def raise_on_failure(exception):
    def decorator(f):
        def wrapper(*args, **kwargs):

            try:
                return f(*args, **kwargs)
            except Exception as e:
                raise exception(e)

        return wrapper
    return decorator
