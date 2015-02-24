"""
    service_factory.providers.basehttp
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module define service provider based on the BaseHTTPHandler.

    :copyright: (c) 2015 by Artem Malyshev.
    :license: GPL3, see LICENSE for more details.
"""

from __future__ import (
    absolute_import, unicode_literals, division, print_function)
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from service_factory.errors import parse_error
from service_factory.exceptions import ServiceException


class HTTPRequestHandler(BaseHTTPRequestHandler):

    protocol_version = 'HTTP/1.1'
    error_message_format = ''

    def log_request(self, *args):
        """Ignore non error logging messages."""

        pass

    def do_POST(self):
        try:
            content_len = self.headers.get('content-length')
            if content_len.isnumeric():  # FIXME: not work
                data = self.rfile.read(int(content_len))
                data = data.decode('utf-8')
                status, response = self.server.service(data)
            else:
                parse_error()
        except ServiceException as error:
            status, response = error.args

        response = response.encode('utf-8')
        self.send_response(status)
        self.send_header("Content-Length", len(response))
        self.end_headers()
        self.wfile.write(response)


class HTTPServiceProvider(HTTPServer):
    """Base HTTP service provider."""

    def __init__(self, service, host, port, allowed_hosts, *args, **kwargs):

        self.service = service
        self.host = host
        self.port = port
        self.allowed_hosts = allowed_hosts
        HTTPServer.__init__(
            self,
            (self.host, self.port),
            HTTPRequestHandler,
            *args, **kwargs)
