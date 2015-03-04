from __future__ import (
    absolute_import, unicode_literals, division, print_function)

import socket
from json import loads

from service_factory.exceptions import ServiceException
from service_factory.providers.basehttp import HTTPServiceProvider


# Helpers.


def make_server(service):
    """Make default server with given server.

    This command doesn't bind and activate server socket.
    """

    return HTTPServiceProvider(service, 'localhost', 9000, ())


def send(addr, *body):
    """Connect to the address, send body."""

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(addr)
    connection.sendall('\r\n'.join(body).encode())
    return connection


def recv(connection):
    """Receive response from connection, close connection."""

    response = connection.recv(65535)
    connection.close()
    return response.decode().split('\r\n')


# Tests.


def test_post_request():
    """Check server can handle single post request."""

    server = make_server(lambda x: (200, x))
    connection = send(
        ('localhost', 9000),
        'POST / HTTP/1.1',
        'Host: localhost:8888',
        'Content-Type:application/json;',
        'Content-Length: 62',
        '',
        '{"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1}',
        '')
    server.handle_request()
    response = recv(connection)
    assert 'HTTP/1.1 200 OK' in response
    assert 'Content-Length: 62' in response
    assert '' in response
    assert ('{"jsonrpc": "2.0", "method": "add", '
            '"params": [1, 2], "id": 1}') in response
    server.server_close()


def test_missed_content_length():
    """Check server can handle single post request."""

    server = make_server(lambda x: (200, x))
    connection = send(
        ('localhost', 9000),
        'POST / HTTP/1.1',
        'Host: localhost:8888',
        'Content-Type:application/json;',
        '',
        '{"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1}',
        '')
    server.handle_request()
    response = recv(connection)
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
    server.server_close()


def test_log_traceback(capsys):
    """Check that we log tracebacks occurs in service."""

    def app(*args, **kwargs):
        raise ServiceException(0, '')
    server = make_server(app)
    connection = send(
        ('localhost', 9000),
        'POST / HTTP/1.1',
        'Host: localhost:8888',
        'Content-Type:application/json;',
        'Content-Length: 62',
        '',
        '{"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1}',
        '')
    server.handle_request()
    recv(connection)
    out, err = capsys.readouterr()
    assert 'ServiceException' in err
    server.server_close()


def test_port_auto_binding(capsys):
    """Check we can select port automatically."""

    service = lambda x: x
    server_a = HTTPServiceProvider(service, 'localhost', 9000, ())
    server_b = HTTPServiceProvider(service, 'localhost', 9001, ())
    server_c = HTTPServiceProvider(service, 'localhost', 'auto', ())
    assert 9002 == server_c.port
    server_a.server_close()
    server_b.server_close()
    server_c.server_close()


def test_port_report(capsys):
    """Check we report used port numder in case of automatic port binding."""

    service = lambda x: x
    server = HTTPServiceProvider(service, 'localhost', 'auto', ())
    out, err = capsys.readouterr()
    assert 'service factory port 9000' in out
    server.server_close()
