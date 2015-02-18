"""
    service_factory.errors
    ~~~~~~~~~~~~~~~~~~~~~~

    This module implements different errors emitters.

    :copyright: (c) 2015 by Artem Malyshev.
    :license: GPL3, see LICENSE for more details.
"""

from __future__ import (
    absolute_import, unicode_literals, division, print_function)
from json import dumps

from .exceptions import ServiceException


def error_emitter(func):
    """Wrap given function into error emitter."""

    def wrapper(*args, **kwargs):
        status_code, response_body = func(*args, **kwargs)
        raise ServiceException(status_code, dumps(response_body))

    return wrapper


@error_emitter
def parse_error():
    """JSON-RPC parse error."""

    response = {
        'jsonrpc': '2.0',
        'id': None,
        'error': {
            'code': -32700,
            'message': 'Parse error',
        },
    }
    return 400, response


@error_emitter
def invalid_request(error):
    """JSON-RPC invalid request error.

    :param error: request error
    :type error: Exception

    """

    response = {
        'jsonrpc': '2.0',
        'id': None,
        'error': {
            'code': -32600,
            'message': 'Invalid Request',
            'data': repr(error),
        },
    }
    return 400, response


@error_emitter
def method_not_found(request_id):
    """JSON-RPC method not found error.

    :param request_id: JSON-RPC request id
    :type request_id: int or str or None

    """

    response = {
        'jsonrpc': '2.0',
        'id': request_id,
        'error': {
            'code': -32601,
            'message': 'Method not found',
        },
    }
    return 400, response


@error_emitter
def server_error(request_id, error):
    """JSON-RPC server error.

    :param request_id: JSON-RPC request id
    :type request_id: int or str or None
    :param error: server error
    :type error: Exception

    """

    response = {
        'jsonrpc': '2.0',
        'id': request_id,
        'error': {
            'code': -32000,
            'message': 'Server error',
            'data': repr(error),
        },
    }
    return 500, response
