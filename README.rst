===================
python-fieldclimate
===================

A client for the iMetos FieldClimate API: https://api.fieldclimate.com/v1/docs/

To use this, you'll need HMAC credentials provided by iMetos. See their docs for more info.

Requires Python 3.6. Uses `aiohttp`, `requests`, and `pycrypto` libraries.

Usage
-----

Asynchronously (recommended):

    >>> import asyncio
    >>> from fieldclimate import FieldClimateAsync
    >>> async def print_user_json():
    ...     async with FieldClimateAsync(public_key='YOUR', private_key='KEYS') as client:
    ...         user = await client.get_user()
    ...         print(user)
    ...
    >>> asyncio.get_event_loop().run_until_complete(print_user_json())
    {'username': '...', }

Synchronously:

    >>> from fieldclimate import FieldClimateSync
    >>> client = FieldClimateSync(public_key='YOUR', private_key='KEYS')
    >>> print(client.get_user())
    {'username': '...', }

You can also specify your hmac keys via the environment variables
`FIELDCLIMATE_PUBLIC_KEY` and `FIELDCLIMATE_PRIVATE_KEY`.
