from __future__ import (
    absolute_import, unicode_literals, division, print_function)
from io import BytesIO
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from service_factory.providers.basehttp import HTTPServiceProvider


# Helpers.


def make_request(*lines):
    """Make request object."""

    rfile = BytesIO('\r\n'.join(lines).encode())
    wfile = Mock()

    def makefile(mode, size):

        if mode == 'rb':
            return rfile
        else:
            return wfile

    kwargs = {'makefile.side_effect': makefile}

    return Mock(**kwargs), rfile, wfile


# Tests.


def test_post_request():
    """Check server can handle single post request."""

    echo_service = lambda x: (200, x)
    server = HTTPServiceProvider(
        echo_service,
        'localhost',
        8888,
        (),
        bind_and_activate=False)
    request, rfile, wfile = make_request(
        'POST / HTTP/1.1',
        'User-Agent: curl/7.35.0',
        'Host: localhost:8888',
        'Accept: */*',
        'Content-type:application/json;',
        'Content-Length: 62',
        '',
        '{"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1}',
        '')
    server.process_request(request, 'localhost')
    # wfile.write.mock_calls
