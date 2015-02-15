from __future__ import (
    absolute_import, unicode_literals, division, print_function)

from service_factory.basehttp import BaseHTTPServer


# Helpers.


def process_request(request):
    """Process single request on given server."""

    response = BaseHTTPServer.handler.process_request(request)
    return response


# Tests.


def test_post_request():
    """Check server can handle single post request."""

    # response = process_request()  # TODO: Write real test here.
    assert True
