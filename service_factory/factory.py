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


def service_factory(app, provider_cls=HTTPServiceProvider, *args, **kwargs):
    """Create service, start server.

    :param app: application to instantiate a service
    :param provider_cls: server class provide a service
    :param args: positional args passed to provider constructor
    :param kwargs: keyword args passed to provider constructor

    """

    service = Service(app)
    server = provider_cls(service, *args, **kwargs)
    server.serve_forever()
