from __future__ import (
    absolute_import, unicode_literals, division, print_function)
from socket import socket

import pytest

from service_factory.providers.basehttp import (
    HTTPRequestHandler, HTTPServiceProvider)


@pytest.skip('Not work yet')
def test_post_request():
    """Check server can handle single post request."""

    echo_service = lambda x: x
    server = HTTPServiceProvider(
        echo_service,
        ('localhost', 8888),
        HTTPRequestHandler,
        bind_and_activate=False)
    request = socket()
    server.process_request(request, 'localhost')
