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

        args = loads(arg)
        method = self.app[args['method']]
        result = method(*args['params'])
        reply = {'jsonrpc': '2.0', 'id': args['id'], 'result': result}
        return dumps(reply)
