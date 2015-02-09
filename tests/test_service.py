from service_factory.service import Service
from json import loads, dumps


def test_call():
    """Check if we can call the service."""
    def add(a, b):
        return a + b
    service = Service([add])
    args = dumps({'jsonrpc': '2.0', 'method': 'add',
                  'params': [1, 2], 'id': 1})
    expected = {'jsonrpc': '2.0', 'result': 3, 'id': 1}
    response_code, response_body = service(args)
    assert (200, expected) == (response_code, loads(response_body))


def test_dict_app():
    """Check we can define service as a dictionary."""

    service = Service({'add': lambda a, b: a + b})
    args = dumps({'jsonrpc': '2.0', 'method': 'add',
                  'params': [1, 2], 'id': 1})
    expected = {'jsonrpc': '2.0', 'result': 3, 'id': 1}
    response_code, response_body = service(args)
    assert (200, expected) == (response_code, loads(response_body))


def test_invalid_request():
    """Check we process invalid requests correctly."""

    service = Service({'add': lambda a, b: a + b})
    args = """{'method': 'name' """
    assert (400, '') == service(args)  # FIXME: Correct response body
    # accordingly to specification.


def test_application_error():
    """Check service can handle application errors."""

    def err():
        raise Exception('We are here.')
    service = Service([err])
    args = dumps({'jsonrpc': '2.0', 'method': 'err', 'params': [], 'id': 1})
    expected = {
        'jsonrpc': '2.0',
        'error': {
            'code': 1,
            'message': "Exception('We are here.',)",
        },
        'id': 1,
    }
    response_code, response_body = service(args)
    assert (500, expected) == (response_code, loads(response_body))


# TODO: log traceback.
# TODO: validate jsonrpc request.
# TODO: unknown method.
