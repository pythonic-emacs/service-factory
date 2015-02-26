from __future__ import (
    absolute_import, unicode_literals, division, print_function)
from io import BytesIO
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from six.moves import reduce

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


def read_response(wfile):
    """Read response written into wfile."""

    calls = wfile.write.mock_calls
    lines = map(lambda x: x[1][0], calls)
    text = reduce(lambda x, y: x + y, lines).decode()
    return text.split('\r\n')


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
        'Host: localhost:8888',
        'Content-Type:application/json;',
        'Content-Length: 62',
        '',
        '{"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1}',
        '')
    server.process_request(request, 'localhost')
    response = read_response(wfile)
    assert 'HTTP/1.1 200 OK' in response
    assert 'Content-Length: 62' in response
    assert '' in response
    assert ('{"jsonrpc": "2.0", "method": "add", '
            '"params": [1, 2], "id": 1}') in response
