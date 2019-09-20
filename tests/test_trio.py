from unittest import TestCase

import trio

from fieldclimate import FieldClimateClient
from tests.utils import trio_test


class TrioTestCase(TestCase):
    """Testing TrioTestCase requires valid HMAC keys to be set via
    the FIELDCLIMATE_PUBLIC_KEY and FIELDCLIMATE_PRIVATE_KEY variables."""

    @trio_test
    async def test_trio_simple_example(self):
        client = FieldClimateClient()
        return await client.get_user()

    @trio_test
    async def test_trio_advanced_example(self):
        async with FieldClimateClient(connections=20) as client:

            async def print_user_json():
                print(await client.get_user())

            async def print_station_dates(station):
                print(await client.get_data_range(station))

            async def count_stations_then_print_ranges(nursery):
                stations = await client.get_user_stations()
                print(len(stations))
                for station in stations[:10]:
                    nursery.start_soon(print_station_dates, station)

            async with trio.open_nursery() as nursery:
                nursery.start_soon(print_user_json)
                nursery.start_soon(count_stations_then_print_ranges, nursery)
