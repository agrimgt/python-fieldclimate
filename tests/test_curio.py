from unittest import TestCase

import curio

from fieldclimate import FieldClimateClient
from tests.utils import curio_test


class CurioTestCase(TestCase):
    """Testing CurioTestCase requires valid HMAC keys to be set via
    the FIELDCLIMATE_PUBLIC_KEY and FIELDCLIMATE_PRIVATE_KEY variables."""

    @curio_test
    async def test_curio_simple_example(self):
        client = FieldClimateClient()
        return await client.get_user()

    @curio_test
    async def test_curio_advanced_example(self):
        async with FieldClimateClient(connections=20) as client:

            async def print_user_json():
                print(await client.get_user())

            async def print_station_dates(station):
                print(await client.get_data_range(station))

            async def count_stations_then_print_ranges():
                stations = await client.get_user_stations()
                print(len(stations))
                await curio.gather(
                    [
                        (await curio.spawn(print_station_dates, station))
                        for station in stations[:10]
                    ]
                )

            await curio.gather(
                [
                    (await curio.spawn(print_user_json)),
                    (await curio.spawn(count_stations_then_print_ranges)),
                ]
            )
