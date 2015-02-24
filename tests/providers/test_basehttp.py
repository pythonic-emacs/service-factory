from __future__ import (
    absolute_import, unicode_literals, division, print_function)
from io import BytesIO

from service_factory.providers.basehttp import (
    HTTPRequestHandler, HTTPServiceProvider)


# Helpers.


def make_request(*lines):
    """Make request object."""

    class RequestMock(object):

        def __init__(self, request):

            self.request = request

        def makefile(self, mode, size):

            if mode == 'rb':
                return BytesIO(self.request)
            else:
                return BytesIO()

        def close(self, *args, **kwargs):

            pass

        def shutdown(self, *args, **kwargs):

            pass

    content = '\r\n'.join(lines).encode()
    return RequestMock(content)


# Tests.


def test_post_request():
    """Check server can handle single post request."""

    echo_service = lambda x: x
    server = HTTPServiceProvider(
        echo_service,
        'localhost',
        8888,
        (),
        bind_and_activate=False)
    request = make_request()
    server.process_request(request, 'localhost')
