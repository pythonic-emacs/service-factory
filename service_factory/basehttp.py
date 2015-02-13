"""
    service_factory.basehttp
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This module define service provider based on the BaseHTTPHandler.

    :copyright: (c) 2015 by Artem Malyshev.
    :license: GPL3, see LICENSE for more details.
"""

from __future__ import (
    absolute_import, unicode_literals, division, print_function)


class BaseHTTPServer(object):
    """Service provider based on BaseHTTPHandler."""

    def __init__(self, service, host, port, allowed_hosts):

        self.service = service
        self.host = host
        self.port = port
        self.allowed_hosts = allowed_hosts
