===================
python-fieldclimate
===================

A client for the iMetos FieldClimate API: https://api.fieldclimate.com/v1/docs/

To use this, you'll need HMAC credentials provided by iMetos. See their docs for more info.

Requires Python 3.6. Uses aiohttp_ and pycryptodome_.

.. _aiohttp: https://github.com/aio-libs/aiohttp
.. _pycryptodome: https://github.com/Legrandin/pycryptodome


Installation
------------

Use ``pip`` to install directly from PyPI_::

  pip install python-fieldclimate

.. _PyPI: https://pypi.org/project/python-fieldclimate/


Authentication
--------------

HMAC credentials can be provided in three ways:

1. Via the init constructor:

   >>> FieldClimateClient(public_key='YOUR', private_key='KEYS')

2. Environment variables ``FIELDCLIMATE_PUBLIC_KEY`` and ``FIELDCLIMATE_PRIVATE_KEY``
   (You can override these variable names too).

3. Subclassing FieldClimateClient:

   >>> class MyClient(FieldClimateClient):
   ...     private_key = 'YOUR'
   ...     public_key = 'KEYS'


Usage
-----

The same FieldClimateClient class can be used to make synchronous and asynchronous requests.
This way, the code you write can be free of async/await syntax until you decide you need it.

Here are some short examples to get you up and running. There are longer examples in `When to Use Async`_.

Synchronous Usage:

>>> from fieldclimate import FieldClimateClient
>>>
>>> client = FieldClimateClient(private_key='YOUR', public_key='KEYS')
>>> client.get_user()
{'username': 'you!', ...}


Asynchronous Usage:

>>> from asyncio import run
>>> from fieldclimate import FieldClimateClient
>>>
>>> async def main():
>>>     async with FieldClimateClient(private_key='YOUR', public_key='KEYS') as client:
>>>         return await client.get_user()
>>>
>>> run(main)
{'username': 'also you!', ...}


It achieves this by calling running an asyncio loop internally if it finds itself under an asynchronous context manager.
In other words, if you *don't* use the client in an `async with` block, you don't have to await the client methods.


Methods
~~~~~~~

The client has methods for each of the corresponding routes listed in the api docs.
There's a lot of them, so see the full list of methods in ``fieldclimate/__init__.py`` for more details.

These methods do not have test coverage (and some, like ``delete_user()``, could be dangerous!).
However, the underlying logic and utilities they use are all tested.

Every method returns a dictionary response.

Some methods will clean up their arguments in order to make working with the api in python easier.
Here are some examples:

- ``get_data_last()`` accepts the ``time_period`` parameter.
  The API docs specify this to be a string like ``'6h'`` or ``'7d'``, meaning 6 hours or 7 days.
  FieldClimateClient additionally accepts timedelta objects for this parameter,
  and will convert them to their equivalent strings for the API
  (i.e. ``timedelta(hours=6)`` is converted to ``'21600'`` seconds).

- Many methods require a ``station`` parameter, like ``get_data_range()`` does in the examples above.
  This can be a raw Station ID string, which you can dig out of a station dictionary returned by ``get_user_stations()``.
  Or, you can pass that dictionary directly in as the station parameter, and the ID will be extracted.

- More method parameter cleaners can be found in ``fieldclimate/utils.py``.


When to Use Async
~~~~~~~~~~~~~~~~~

Synchronous code is easier to read, but Python can potentially spend more time waiting when running it.

This script finishes in 12.9 seconds:

.. code-block:: python

   from fieldclimate import FieldClimateClient

   def main():
       client = FieldClimateClient()
       # print user json
       print(client.get_user())
       # count stations
       stations = client.get_user_stations()
       print(len(stations))
       # print ranges
       for station in stations[:10]:
           print(client.get_data_range(station))

   if __name__ == '__main__':
       main()

output:

>>> main()
{'username': '...', }
1337
{'min_date': '2016-04-27 12:33:37', 'max_date': '2018-10-23 16:00:08'}
{'min_date': '2016-05-05 10:00:13', 'max_date': '2018-10-09 23:00:04'}
{'min_date': '2016-04-27 12:54:09', 'max_date': '2018-09-18 12:14:50'}
{'min_date': '2016-04-27 12:43:29', 'max_date': '2018-09-23 11:00:03'}
{'min_date': '2016-03-24 01:16:40', 'max_date': '2018-10-23 15:55:09'}
{'min_date': '2016-04-27 11:52:15', 'max_date': '2018-10-19 15:00:08'}
{'min_date': '2016-04-28 04:02:11', 'max_date': '2018-10-23 16:00:08'}
{'min_date': '2015-11-16 01:05:32', 'max_date': '2018-10-23 16:00:08'}
{'min_date': '2016-04-27 11:34:52', 'max_date': '2018-10-11 20:00:03'}
{'min_date': '2016-06-01 19:00:27', 'max_date': '2018-09-06 16:00:38'}


Asynchronous mode works by using the client as an async context manager.
Async code is more complicated, but allows a lot of work to be done at once.

This script finishes in 3.9 seconds:

.. code-block:: python

   import asyncio
   from fieldclimate import FieldClimateClient

   async def main():
       async with FieldClimateClient() as client:

           async def print_user_json():
               print(await client.get_user())

           async def print_station_dates(station):
               print(await client.get_data_range(station))

           async def count_stations_then_print_ranges():
               stations = await client.get_user_stations()
               print(len(stations))
               await asyncio.gather(*[
                   print_station_dates(station)
                   for station in stations[:10]
               ])

           await asyncio.gather(
               print_user_json(),
               count_stations_then_print_ranges(),
           )

   if __name__ == '__main__':
       asyncio.run(main())

output:

>>> asyncio.run(main())
{'username': '...', }
1337
{'min_date': '2016-04-27 11:52:15', 'max_date': '2018-10-19 15:00:08'}
{'min_date': '2016-04-27 12:54:09', 'max_date': '2018-09-18 12:14:50'}
{'min_date': '2015-11-16 01:05:32', 'max_date': '2018-10-23 16:00:08'}
{'min_date': '2016-04-27 12:43:29', 'max_date': '2018-09-23 11:00:03'}
{'min_date': '2016-04-27 12:33:37', 'max_date': '2018-10-23 16:00:08'}
{'min_date': '2016-06-01 19:00:27', 'max_date': '2018-09-06 16:00:38'}
{'min_date': '2016-04-28 04:02:11', 'max_date': '2018-10-23 16:00:08'}
{'min_date': '2016-03-24 01:16:40', 'max_date': '2018-10-23 15:55:09'}
{'min_date': '2016-05-05 10:00:13', 'max_date': '2018-10-09 23:00:04'}
{'min_date': '2016-04-27 11:34:52', 'max_date': '2018-10-11 20:00:03'}

Notice how the ordering of the dates is different than before.
They are now sorted from the fastest server response to the slowest.
Theoretically, the `{'username':}` line could be printed last.


A note on rate limits
~~~~~~~~~~~~~~~~~~~~~

According to FieldClimate's docs, they do not yet enforce rate limiting server-side.
Using python-fieldclimate asynchronously allows you to create hundreds or thousands of requests at once.
During my testing I noticed the API starting to raise 502 errors when I overloaded it too much.

Please be courteous with your resource consumption!


Contributing
------------

Pull requests are welcome. Please clean your code with black_, write tests, and document.

.. _black: https://github.com/ambv/black

Ideas for PRs:

- Rate limiting with sane defaults.
- Proposals for higher level interfaces, e.g. ``client.stations[i].date_range``.
- Exhaustive mocking to achieve full FC method coverage.
- More parameter-cleaning utils.
