from __future__ import (
    absolute_import, unicode_literals, division, print_function)
from io import BytesIO
from json import loads
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from service_factory.exceptions import ServiceException
from service_factory.providers.basehttp import HTTPServiceProvider


# Helpers.


def make_server(service):
    """Make default server with given server.

    This command doesn't bind and activate server socket.
    """

    return HTTPServiceProvider(
        service,
        'localhost',
        8888,
        (),
        bind_and_activate=False)


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
    text = b''.join(lines).decode()
    return text.split('\r\n')


# Tests.


def test_post_request():
    """Check server can handle single post request."""

    server = make_server(lambda x: (200, x))
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


def test_missed_content_length():
    """Check server can handle single post request."""

    server = make_server(lambda x: (200, x))
    request, rfile, wfile = make_request(
        'POST / HTTP/1.1',
        'Host: localhost:8888',
        'Content-Type:application/json;',
        '',
        '{"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1}',
        '')
    server.process_request(request, 'localhost')
    response = read_response(wfile)
    message = response[-1]
    assert 'HTTP/1.1 400 Bad Request' in response
    assert 'Content-Length: {0}'.format(len(message)) in response
    assert '' in response
    assert loads(message) == {
        'jsonrpc': '2.0',
        'id': None,
        'error': {
            'code': -32700,
            'message': 'Parse error',
        },
    }


def test_log_traceback(capsys):
    """Check that we log tracebacks occurs in service."""

    def app(*args, **kwargs):
        raise ServiceException(0, '')
    server = make_server(app)
    request, rfile, wfile = make_request(
        'POST / HTTP/1.1',
        'Host: localhost:8888',
        'Content-Type:application/json;',
        'Content-Length: 62',
        '',
        '{"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1}',
        '')
    server.process_request(request, 'localhost')
    out, err = capsys.readouterr()
    assert 'ServiceException' in err
