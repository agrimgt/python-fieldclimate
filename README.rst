===================
python-fieldclimate
===================

A client for the iMetos FieldClimate API: https://api.fieldclimate.com/v1/docs/

To use this, you'll need HMAC credentials provided by iMetos. See their docs for more info.

Requires Python 3.5 or better. Tested on Python 3.6. Depends on asks_ and pycryptodome_.

.. _asks: https://github.com/theelous3/asks
.. _pycryptodome: https://github.com/Legrandin/pycryptodome


Installation
------------

Use ``pip`` to install the current release, version 1.3, from PyPI_::

  pip install python-fieldclimate

.. _PyPI: https://pypi.org/project/python-fieldclimate/


Usage
-----

Here's a simple example that returns the associated user's account info:

.. code-block:: python

   from asyncio import run
   from fieldclimate import FieldClimateClient

   async def main():
       async with FieldClimateClient(private_key="YOUR", public_key="KEYS") as client:
           return await client.get_user()

   if __name__ == "__main__":
       run(main)


Event Loops
~~~~~~~~~~~

**New in version 1.3.**

The same FieldClimateClient class can be used to make asynchronous API requests under any modern event loop.
This is thanks to asks being written with anyio_, which currently supports asyncio_, curio_, and trio_.

.. _anyio: https://github.com/agronholm/anyio
.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _curio: https://github.com/dabeaz/curio
.. _trio: https://github.com/python-trio/trio


Authentication
~~~~~~~~~~~~~~

HMAC credentials can be provided in several ways:

1. Via the init constructor:

   >>> FieldClimateClient(public_key="YOUR", private_key="KEYS")

2. Environment variables ``FIELDCLIMATE_PUBLIC_KEY`` and ``FIELDCLIMATE_PRIVATE_KEY``.

3. Subclassing FieldClimateClient:

   >>> class MyClient(FieldClimateClient):
   ...     private_key = "YOUR"
   ...     public_key = "KEYS"

4. If you use Django, you can use ``fieldclimate.django.DjangoFieldClimateClient`` in place of FieldClimateClient.
   This subclass will grab ``FIELDCLIMATE_PUBLIC_KEY`` and ``FIELDCLIMATE_PRIVATE_KEY`` from django's settings.


Methods
~~~~~~~

The client has methods for each of the corresponding routes listed in the api docs.
There's a lot of them, so see the full list of methods in ``fieldclimate/__init__.py`` for more details.
Every method returns a JSON-like python object upon being awaited, like a dictionary or a list.

Some methods will clean up their arguments in order to make working with the API in python easier.
Here are some examples:

- ``get_data_last()`` accepts the ``time_period`` parameter.
  The API docs specify this to be a string like ``'6h'`` or ``'7d'``, meaning 6 hours or 7 days.
  FieldClimateClient additionally accepts timedelta objects for this parameter,
  and will convert them to their equivalent strings for the API
  (i.e. ``timedelta(hours=6)`` is converted to ``'21600'`` seconds).

- Many methods require a ``station`` parameter, like ``get_data_range()`` does in the examples above.
  This can be a raw Station ID string, which you can dig out of a station dictionary returned by ``get_user_stations()``.
  Or, you can pass that dictionary directly in as the station parameter, and the ID will be extracted.

These methods do not all have test coverage (testing ``delete_user()`` might be a bad idea).
However, the underlying connection and cleaning utilities they use are all tested.


Connection Limits
~~~~~~~~~~~~~~~~~

**New in version 1.3.**

The connection limit can be raised by setting the connections argument when calling the FieldClimateClient constructor.

From `asks' docs`_:

    You *will* want to change the number of connections to a value that suits your needs and the server’s limitations.
    If no data is publicly available to guide you here, err on the low side.

    **The default number of connections in the pool for a Session is a measly ONE.**

.. _asks' docs: https://asks.readthedocs.io/en/latest/a-look-at-sessions.html#important-connection-un-limiting

Example:

.. code-block:: python

   async with FieldClimateClient(connections=10) as client:
       ...


According to FieldClimate's docs, they do not yet enforce rate limiting server-side.
Using FieldClimateClient with a high connection limit allows you to create *a lot* of requests at once.
During my testing, I noticed the API starting to raise 502 errors when I overloaded it too much.

Please be courteous with your resource consumption!


Advanced Example
~~~~~~~~~~~~~~~~

This function asks for some user data and gets the list of all user stations, at the same time.
As soon as the stations come back, it counts them and sends off another request for each of the first 10 stations.
Then each of those 10 station responses is printed, sorted by server reply time.

.. code-block:: python

   from asyncio import gather, run
   from fieldclimate import FieldClimateClient

   async def main():
       async with FieldClimateClient(
           private_key="YOUR",
           public_key="KEYS",
           connections=20
       ) as client:
           async def print_user_json():
               print(await client.get_user())

           async def print_station_dates(station):
               print(await client.get_data_range(station))

           async def count_stations_then_print_ranges():
               stations = await client.get_user_stations()
               print(len(stations))
               await gather(*[
                   print_station_dates(station)
                   for station in stations[:10]
               ])

           await gather(
               print_user_json(),
               count_stations_then_print_ranges(),
           )

   if __name__ == "__main__":
       run(main())


Alternate curio and trio implementations are the ``tests`` directory,
if you want to see how to use FieldClimateClient in those event loops (it's much of the same).


Synchronous Usage
~~~~~~~~~~~~~~~~~

**Removed in version 1.3.**

In version 1.2, FieldClimateClient would automatically set up an asyncio event loop when methods were
being called outside of an ``async with`` block.
This way, callers could use the library without having to write any scary async/await code.

Having this mix of syntax ended up being confusing and unnecessary, in addition to leading to messy code here.
So, with the switch to the ``asks`` backend, support for the old synchronous use case was removed.

If you were using FieldClimateClient's older 'synchronous usage' mode, you were already using a version of Python that
allowed for async/await. The difference is that now you have to set up an event loop yourself.

If you still *really* don't want to write any coroutines, the simplest way to make your code compatible with version 1.3
is to just wrap each method call with ``asyncio.run()``:

.. code-block:: python

   import asyncio
   from fieldclimate import FieldClimateClient

   def main():
       client = FieldClimateClient(private_key="YOUR", public_key="KEYS")
       # print user json
       print(asyncio.run(client.get_user()))
       # count stations
       stations = asyncio.run(client.get_user_stations())
       print(len(stations))
       # print ranges
       for station in stations[:10]:
           print(asyncio.run(client.get_data_range(station)))

   if __name__ == "__main__":
       main()


This 'synchronous' example takes 3 times longer to complete than the equivalent "Advanced Example" above, because the
main() function is blocked during each request sent to the server.
The asynchronous code, on the other hand, only blocks when there's nothing to do *but* wait for the server.
Consider this when deciding whether or not to convert your code to use coroutine functions.


Contributing
------------

Pull requests are welcome. Please clean your code with black_, write tests, and document.

.. _black: https://github.com/ambv/black

Ideas for PRs:

- Exhaustive mocking to achieve full method test coverage.
- OAuth 2.0 authentication.
