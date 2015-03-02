from service_factory import service_factory

def add(one, two):
    """Add two numbers."""
    return one + two

def mul(one, two):
    """Multiply two numbers."""
    return one * two

app = [add, mul]

if __name__ == '__main__':
    service_factory(app, host='localhost', port=9000)
