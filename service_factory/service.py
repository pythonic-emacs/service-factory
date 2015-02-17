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

from .errors import (
    invalid_request, method_not_found, parse_error, server_error)


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
        :raises: ServiceException

        """

        args = self.load_args(arg)
        self.validate(args)
        method = self.get_method(args)
        result = self.apply(method, args)
        response = self.make_response(args, result)
        return 200, response

    def load_args(self, arg):
        """Loads service args from string.

        :param arg: Request body
        :raises: ServiceException

        """

        try:
            args = loads(arg)
        except ValueError:
            parse_error()
        else:
            return args

    def validate(self, request):
        """Validate JSON-RPC request.

        :param request: RPC request object
        :type request: dict

        """

        try:
            self.validate_version(request)
            self.validate_method(request)
            self.validate_params(request)
            self.validate_id(request)
        except (AssertionError, KeyError) as error:
            invalid_request(error)

    def validate_version(self, request):
        """Validate request version."""

        correct_version = request['jsonrpc'] == '2.0'
        error = 'Incorrect version of the JSON-RPC protocol'
        assert correct_version, error

    def validate_method(self, request):
        """Validate request method."""

        correct_method = isinstance(request['method'], six.string_types)
        error = 'Incorrect name of the method to be invoked'
        assert correct_method, error

    def validate_params(self, request):
        """Validate request params."""

        if 'params' in request:
            correct_params = isinstance(request['params'], (list, dict))
            error = 'Incorrect parameter values'
            assert correct_params, error

    def validate_id(self, request):
        """Validate request id."""

        if 'id' in request:
            correct_id = isinstance(
                request['id'],
                (six.string_types, int, None))
            error = 'Incorrect identifier'
            assert correct_id, error

    def get_method(self, args):
        """Get request method for service application."""

        try:
            method = self.app[args['method']]
        except KeyError:
            method_not_found(args['id'])
        else:
            return method

    def apply(self, method, args):
        """Apply application method."""

        try:
            params = args['params']
            if isinstance(params, dict):
                result = method(**params)
            else:
                result = method(*params)
        except Exception as error:
            server_error(args['id'], error)
        else:
            return result

    def make_response(self, args, result):
        """Create response body from given result."""

        return dumps({
            'jsonrpc': '2.0',
            'id': args['id'],
            'result': result,
        })
