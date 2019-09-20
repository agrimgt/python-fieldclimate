import asyncio
from unittest import TestCase

from fieldclimate import FieldClimateClient
from tests.utils import async_test


class AsyncioTestCase(TestCase):
    """Testing AsyncioTestCase requires valid HMAC keys to be set via
    the FIELDCLIMATE_PUBLIC_KEY and FIELDCLIMATE_PRIVATE_KEY variables."""

    @async_test
    async def test_asyncio_simple_example(self):
        client = FieldClimateClient()
        return await client.get_user()

    @async_test
    async def test_asyncio_advanced_example(self):
        async with FieldClimateClient(connections=20) as client:

            async def print_user_json():
                print(await client.get_user())

            async def print_station_dates(station):
                print(await client.get_data_range(station))

            async def count_stations_then_print_ranges():
                stations = await client.get_user_stations()
                print(len(stations))
                await asyncio.gather(
                    *[print_station_dates(station) for station in stations[:10]]
                )

            await asyncio.gather(print_user_json(), count_stations_then_print_ranges())
