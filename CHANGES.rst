=======
Changes
=======


2.0 (2019-09-18)
----------------

- Moved url validation functions from ``fieldclimate.utils`` to ``fieldclimate.clean``.
  These functions now ``raise AssertionError()`` explicitly.
  Before, ``assert``s were compiled out during production.
- Dropped ``aiohttp`` dependency in favor of ``asks``.
- This means python-fieldclimate now supports asyncio, trio, and curio async loops!
- FieldClimateClient now inherits from ``asks.Session``,
  which provides async context manager usage and connection rate limiting.
- Removed BaseClient and HmacClient classes, unifying their functionality in FieldClimateClient.
- Dropped synchronous method interface, meaning all client methods must now be awaited.
- Rewrote README.rst with new changes.
- Added tests for trio and curio event loops.
- Added DjangoFieldClimateClient.


1.2 (2018-10-26)
----------------

- Dropped ``requests`` library in favor of using ``aiohttp`` for both sync and async interfaces.


1.1 (2018-10-25)
----------------

- Renamed all ``station_id`` method parameters to ``station``, possibly breaking your code.
- This argument can now handle an entire station dictionary, and will extract the station_id automatically.


1.0 (2018-10-24)
----------------

- Initial PyPI release. 🎉
