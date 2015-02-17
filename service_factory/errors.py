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


def parse_error():
    """JSON-RPC parse error."""

    response = dumps({
        'jsonrpc': '2.0',
        'id': None,
        'error': {
            'code': -32700,
            'message': 'Parse error',
        },
    })
    raise ServiceException(400, response)


def invalid_request(error):
    """JSON-RPC invalid request error.

    :param error: request error
    :type error: Exception

    """

    response = dumps({
        'jsonrpc': '2.0',
        'id': None,
        'error': {
            'code': -32600,
            'message': 'Invalid Request',
            'data': repr(error),
        },
    })
    raise ServiceException(400, response)


def method_not_found(id):
    """JSON-RPC method not found error.

    :param id: JSON-RPC request id
    :type id: int or str or None

    """

    response = dumps({
        'jsonrpc': '2.0',
        'id': id,
        'error': {
            'code': -32601,
            'message': 'Method not found',
        },
    })
    raise ServiceException(400, response)


def server_error(id, error):
    """JSON-RPC server error.

    :param id: JSON-RPC request id
    :type id: int or str or None
    :param error: server error
    :type error: Exception

    """

    response = dumps({
        'jsonrpc': '2.0',
        'id': id,
        'error': {
            'code': -32000,
            'message': 'Server error',
            'data': repr(error),
        },
    })
    raise ServiceException(500, response)
