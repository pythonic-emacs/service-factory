"""
    service_factory.service
    ~~~~~~~~~~~~~~~~~~~~~~~

    This module define service class.

    :copyright: (c) 2015 by Artem Malyshev.
    :license: GPL3, see LICENSE for more details.
"""


class Service(object):
    """Base Service.  Provide application method access."""

    def __init__(self, app):

        self.app = app
