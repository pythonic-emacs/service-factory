"""
    service_factory.service
    ~~~~~~~~~~~~~~~~~~~~~~~

    This module define service class.

    :copyright: (c) 2015 by Artem Malyshev.
    :license: GPL3, see LICENSE for more details.
"""

from json import loads, dumps


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
            method = self.app[args['method']]
        except KeyError:
            return method_not_found(args['id'])

        try:
            result = method(*args['params'])
        except Exception as error:
            return server_error(args['id'], error)

        response = dumps({
            'jsonrpc': '2.0',
            'id': args['id'],
            'result': result,
        })
        return 200, response


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
