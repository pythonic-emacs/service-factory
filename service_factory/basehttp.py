"""
    service_factory.basehttp
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This module define service provider based on the BaseHTTPHandler.

    :copyright: (c) 2015 by Artem Malyshev.
    :license: GPL3, see LICENSE for more details.
"""

from __future__ import (
    absolute_import, unicode_literals, division, print_function)
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class HTTPRequestHandler(BaseHTTPRequestHandler):

    protocol_version = 'HTTP/1.1'
    error_message_format = ''

    def log_request(*args):
        """Ignore non error logging messages."""

        pass

    def do_POST(self):
        content_len = self.headers.get('content-length')
        if content_len is not None:
            data = self.rfile.read(int(content_len))
            data = data.decode('utf-8')
            status, response = self.process_request(data)
        else:
            status, response = 400, 'Missing content-length header'

        response = response.encode('utf-8')
        self.send_response(status)
        self.send_header("Content-Length", len(response))
        self.end_headers()
        self.wfile.write(response)

    def process_request(self, request):
        response = True
        return response


class BaseHTTPServer(object):
    """Service provider based on BaseHTTPHandler."""

    handler = HTTPRequestHandler

    def __init__(self, service, host, port, allowed_hosts):

        self.service = service
        self.host = host
        self.port = port
        self.allowed_hosts = allowed_hosts
