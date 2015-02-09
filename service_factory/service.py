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

        if isinstance(app, list):
            self.app = dict((method.__name__, method) for method in app)
        elif isinstance(app, dict):
            self.app = app

    def __call__(self, arg):
        """Perform jsonrpc call."""

        try:
            args = loads(arg)
        except ValueError:
            return 400, ''
        method = self.app[args['method']]
        try:
            result = method(*args['params'])
        except Exception as error:
            response = dumps({
                'jsonrpc': '2.0',
                'id': args['id'],
                'error': {
                    'code': 1,
                    'message': repr(error),
                },
            })
            return 500, response
        else:
            response = {
                'jsonrpc': '2.0',
                'id': args['id'],
                'result': result,
            }
            return 200, dumps(response)
