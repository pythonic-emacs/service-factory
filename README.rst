===============
service-factory
===============
JSON RPC service factory for Python.

TODO
----

* WSGI support
* customizable message for port number report
* --port-file option

.. code:: bash

    python -m service_factory anaconda_mode:app --iface=localhost --port=auto
    # or
    service_factory 'anaconda_mode:app' --iface=localhost --port=auto

.. code:: python

    # list of callbles
    app = [complete, goto_definitions]

    service_factory(app, iface='localhost', port='auto')
