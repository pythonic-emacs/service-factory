from __future__ import (
    absolute_import, unicode_literals, division, print_function)
from json import loads, dumps

from service_factory.service import Service
from service_factory.exceptions import ServiceException


# Helpers.


def check_response(service, args, status_code, expected_body):
    """Verify response against given arguments.
    Check jsonrpc specification compilance."""

    try:
        code, body = service(args)
    except ServiceException as error:
        code, body = error.args
    reply = loads(body)
    assert code == status_code
    assert reply['jsonrpc'] == '2.0'
    assert 'id' in reply
    assert 'result' in reply or 'error' in reply
    assert 'error' not in reply if 'result' in reply else True
    assert 'result' not in reply if 'error' in reply else True
    assert reply == expected_body


# Tests.


def test_call():
    """Check if we can call the service."""
    def add(a, b):
        return a + b
    service = Service([add])
    args = dumps({
        'jsonrpc': '2.0',
        'method': 'add',
        'params': [1, 2],
        'id': 1,
    })
    check_response(service, args, 200, {
        'jsonrpc': '2.0',
        'result': 3,
        'id': 1
    })


def test_dict_app():
    """Check we can define service as a dictionary."""

    service = Service({'add': lambda a, b: a + b})
    args = dumps({
        'jsonrpc': '2.0',
        'method': 'add',
        'params': [1, 2],
        'id': 1,
    })
    check_response(service, args, 200, {
        'jsonrpc': '2.0',
        'result': 3,
        'id': 1
    })


def test_parse_error():
    """Check we can process parse errors correctly."""

    service = Service({'add': lambda a, b: a + b})
    args = """{'method': 'name' """
    check_response(service, args, 400, {
        'jsonrpc': '2.0',
        'error': {
            'code': -32700,
            'message': 'Parse error',
        },
        'id': None,
    })


def test_application_error():
    """Check service can handle application errors."""

    def err():
        raise Exception('We are here.')
    service = Service([err])
    args = dumps({'jsonrpc': '2.0', 'method': 'err', 'params': [], 'id': 1})
    check_response(service, args, 500, {
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'message': 'Server error',
            'data': repr(Exception('We are here.')),
        },
        'id': 1,
    })


def test_method_not_found():
    """Service must handle unknown method requests."""

    service = Service({})
    args = dumps({
        'jsonrpc': '2.0',
        'method': 'add',
        'params': [1, 2],
        'id': 1,
    })
    check_response(service, args, 400, {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found',
        },
        'id': 1,
    })


def test_dict_params():
    """Check we can use dictionary in params field."""

    service = Service({'add': lambda x, y: x + y})
    args = dumps({
        'jsonrpc': '2.0',
        'method': 'add',
        'params': {
            'x': 1,
            'y': 2,
        },
        'id': 1,
    })
    check_response(service, args, 200, {
        'jsonrpc': '2.0',
        'result': 3,
        'id': 1
    })


def test_invalid_request():
    """Check we can process invalid requests correctly"""

    service = Service({'add': lambda x, y: x + y})
    args = dumps({
        'jsonrpc': '2.0',
        'method': 1,
        'params': 'bar',
    })
    check_response(service, args, 400, {
        'jsonrpc': '2.0',
        'error': {
            'code': -32600,
            'message': 'Invalid Request',
            'data': repr(
                AssertionError(
                    'Incorrect name of the method to be invoked')),
        },
        'id': None,
    })
