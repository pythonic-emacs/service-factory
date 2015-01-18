
.. |travis| image:: https://travis-ci.org/proofit404/service-factory.png
    :target: https://travis-ci.org/proofit404/service-factory
    :alt: Build Status

.. |coveralls| image:: https://coveralls.io/repos/proofit404/service-factory/badge.png
    :target: https://coveralls.io/r/proofit404/service-factory
    :alt: Coverage Status

.. |requires| image:: https://requires.io/github/proofit404/service-factory/requirements.svg
    :target: https://requires.io/github/proofit404/service-factory/requirements
    :alt: Requirements Status

.. |landscape| image:: https://landscape.io/github/proofit404/service-factory/master/landscape.svg
    :target: https://landscape.io/github/proofit404/service-factory/master
    :alt: Code Health

===============
service-factory
===============

|travis| |coveralls| |requires| |landscape|

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
