from service_factory.service import Service
from json import loads, dumps


def test_call():
    """Check if we can call the service."""
    def add(a, b):
        return a + b
    service = Service([add])
    args = dumps({'jsonrpc': '2.0', 'method': 'add',
                  'params': [1, 2], 'id': 1})
    expected = {'jsonrpc': '2.0', 'result': 3, 'id': 1}
    assert expected == loads(service(args))
