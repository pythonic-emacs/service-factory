"""
    service_factory.service
    ~~~~~~~~~~~~~~~~~~~~~~~

    This module define service class.

    :copyright: (c) 2015 by Artem Malyshev.
    :license: GPL3, see LICENSE for more details.
"""

from __future__ import (
    absolute_import, unicode_literals, division, print_function)
from json import loads, dumps

import six


class Service(object):
    """Base Service.  Provide application method access."""

    def __init__(self, app):
        """Service constructor.

        :param app: application definition
        :type app: list of callable, dict of callable

        """

        if isinstance(app, list):
            self.app = dict((method.__name__, method) for method in app)
        elif isinstance(app, dict):
            self.app = app

    def __call__(self, arg):
        """Perform jsonrpc call.

        :param arg: JSON-RPC request body
        :type arg: str

        """

        try:
            args = loads(arg)
        except ValueError:
            return parse_error()

        try:
            self.validate(args)
        except (AssertionError, KeyError) as error:
            return invalid_request(error)

        try:
            method = self.app[args['method']]
        except KeyError:
            return method_not_found(args['id'])

        try:
            if isinstance(args['params'], dict):
                result = method(**args['params'])
            else:
                result = method(*args['params'])
        except Exception as error:
            return server_error(args['id'], error)

        response = dumps({
            'jsonrpc': '2.0',
            'id': args['id'],
            'result': result,
        })
        return 200, response

    def validate(self, request):
        """Validate JSON-RPC request.

        :param request: RPC request object
        :type request: dict

        """

        correct_version = request['jsonrpc'] == '2.0'
        error = 'Incorrect version of the JSON-RPC protocol'
        assert correct_version, error

        correct_method = isinstance(request['method'], six.string_types)
        error = 'Incorrect name of the method to be invoked'
        assert correct_method, error

        if 'params' in request:
            correct_params = isinstance(request['params'], (list, dict))
            error = 'Incorrect parameter values'
            assert correct_params, error

        if 'id' in request:
            correct_id = isinstance(
                request['id'],
                (six.string_types, int, None))
            error = 'Incorrect identifier'
            assert correct_id, error


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
    return 400, response


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
    return 400, response


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
    return 400, response


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
    return 500, response
