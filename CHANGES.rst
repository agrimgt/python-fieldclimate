=======
Changes
=======


TODO
----

- Add support for Metos' API v2: https://api.fieldclimate.com/v2/docs/
  - How should we best support both users of v2 and v1, which should still be supported?
  - Need to assess how different the new API is before deciding on how to tackle this.
  - Increment major version to track with upstream.


1.3 (2019-09-23)
----------------

High-level changes:

- Dropped ``aiohttp`` library in favor of using ``asks``.
- This adds support for asyncio, trio, and curio async loops.
- Dropped synchronous interface on FieldClimateClient.
  **This means all client methods must now be awaited.**

Implementation changes:

- Moved url validation functions from ``fieldclimate.utils`` to ``fieldclimate.clean``.
  These functions now raise ``AssertionError`` explicitly, as ``assert`` statements can be switched off.
- FieldClimateClient now inherits from ``asks.Session``,
  which provides async context manager usage and connection rate limiting.
- Removed BaseClient and HmacClient classes, unifying their functionality in FieldClimateClient.
- Added tests for trio and curio event loops.

Bonus changes:

- Added DjangoFieldClimateClient.
  This subclass gets your HMAC authentication keys from django's settings,
  which can save you a few lines of code if you already use django.


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
