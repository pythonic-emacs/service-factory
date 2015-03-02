from __future__ import (
    absolute_import, unicode_literals, division, print_function)

from service_factory.factory import service_factory


# Tests.


def test_service_factory():
    """Check service_factory will run given provider."""

    app = [lambda x: x]

    class TestProvider(object):
        def __init__(self, *args, **kwargs):
            pass

        def serve_forever(self):
            pass

    service_factory(app, TestProvider)
