#############
Asynchronizer
#############

.. _description:

**Asynchronizer** is simple module that can be used to run multiple functions asynchronously. To convert a function, you just need to add a decorator :code:`@asynchronize` to the function. This project is still in development, so report any bugs `here <https://github.com/Arsh23/asynchronizer/issues>`_. For example, see the `example folder <https://github.com/Arsh23/asynchronizer/tree/master/examples>`_

.. contents::

.. _requirements:

Requirements
************

- python 2.x **or** python 3.x


.. _installation:

Installation
************

**Asynchronizer** can be installed using pip:

.. code-block:: bash

    pip install asynchronizer

How to use
**********
Basic use
^^^^^^^^^

    Suppose you have a function like this:

            .. code-block:: python

                import requests

                def send_requests():
                    r = requests.get('http://httpbin.org/get')
                    print r.status_code

                for _ in range(20):
                    send_requests()

    You can modify it like this to make it asynchronous:

        .. code-block:: python

                import requests
                from asynchronizer import asynchronize, startPool

                @asynchronize
                def send_requests():
                    r = requests.get('http://httpbin.org/get')
                    print r.status_code

                for _ in range(20):
                    send_requests()

                startPool()

Things to keep in mind
^^^^^^^^^^^^^^^^^^^^^^

    - The function :code:`startPool()` is necessary. If :code:`startPool()` is not present, none of the asynchronous functions will run.

    - The function :code:`startPool()` is also a blocking function, meaning that the execution of your script will pause here till all the async functions called before this are finished. This is why it should usually be added at the end of your script

    - The decorated functions are async to each other, but the code inside the functions is synchronous, which means this is wrong:

        .. code-block:: python

                # wrong way
                @asynchronize
                def send_requests():
                    for _ in range(20):
                        r = requests.get('http://httpbin.org/get')

                send_requests()

       and this is the correct way:

        .. code-block:: python

                # correct way
                @asynchronize
                def send_requests():
                    r = requests.get('http://httpbin.org/get')

                for _ in range(20):
                    send_requests()

    - Instead of returning values from your functions, send them to a callback. For example:

        .. code-block:: python

                @asynchronize
                def send_requests():
                    r = requests.get('http://httpbin.org/get')
                    parse(r.text)
                    # instead of return r.text


Advanced use
^^^^^^^^^^^^

    - If you want to modify how many functions should be called concurrently, just add :code:`setWorkers(n)` at the start of your script, with :code:`n` being the number of concurrent threads. Default is 32.

    - To assign priority to a specific function call, add :code:`priority=n` to the parameters of the function call, with :code:`n` being the priority you want to set. For Example: :code:`func(param1,param2,param3,priority=2)`

Contributing
************

If you want to contribute to this project, feel free to send a Pull Request to `Github <https://github.com/Arsh23/asynchronizer>`_

To report any bugs or request new features, head over to the `Issues <https://github.com/Arsh23/asynchronizer/issues>`_ page

License
*******

Licensed under `The MIT License (MIT) <https://github.com/Arsh23/asynchronizer/blob/master/LICENSE.txt>`_.


Copyright
*********

Copyright (c) 2016 Arsh
