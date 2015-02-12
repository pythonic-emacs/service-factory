"""
    service_factory.factory
    ~~~~~~~~~~~~~~~~~~~~~~~

    This module define service factory.

    :copyright: (c) 2015 by Artem Malyshev.
    :license: GPL3, see LICENSE for more details.
"""

from __future__ import (
    absolute_import, unicode_literals, division, print_function)

from .basehttp import BaseHTTPServer
from .service import Service


def service_factory(app, server_cls=BaseHTTPServer,
                    host='localhost', port='auto',
                    allowed_hosts={}):
    """Create service, start server."""

    service = Service(app)
    server = server_cls(service, host, port, allowed_hosts)
    return server
