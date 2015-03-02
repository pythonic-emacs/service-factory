"""
    service_factory.factory
    ~~~~~~~~~~~~~~~~~~~~~~~

    This module define service factory.

    :copyright: (c) 2015 by Artem Malyshev.
    :license: GPL3, see LICENSE for more details.
"""

from __future__ import (
    absolute_import, unicode_literals, division, print_function)

from .providers.basehttp import HTTPServiceProvider
from .service import Service


def service_factory(app, privider_cls=HTTPServiceProvider,
                    host='localhost', port='auto',
                    allowed_hosts=()):
    """Create service, start server."""

    service = Service(app)
    server = privider_cls(service, host, port, allowed_hosts)
    server.serve_forever()
