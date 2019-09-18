import asyncio
import os
from unittest import TestCase, mock

from fieldclimate import FieldClimateClient
from tests.utils import async_test

INVALID_KEYS = {
    "FIELDCLIMATE_PUBLIC_KEY": "invalid",
    "FIELDCLIMATE_PRIVATE_KEY": "invalid",
}
UNAUTHORIZED = {
    "message": (
        "Unauthorized. The request requires user authentication, "
        "refer to documentation for more information."
    )
}


class FieldClimateTestCase(TestCase):
    """Testing FieldClimateTestCase requires valid HMAC keys to be set via
    the FIELDCLIMATE_PUBLIC_KEY and FIELDCLIMATE_PRIVATE_KEY variables.

    For now, tests are limited to viewing the user profile. It would be
    nice to have tests the rest of the methods, but I really don't want
    to muck about with a live account...
    """

    def test_all_keys_are_set(self):
        self.assertIn("FIELDCLIMATE_PUBLIC_KEY", os.environ)
        self.assertIn("FIELDCLIMATE_PRIVATE_KEY", os.environ)

    @mock.patch.dict("os.environ", INVALID_KEYS)
    @async_test
    async def test_unauthorized(self):
        user = await FieldClimateClient().get_user()
        self.assertDictEqual(user, UNAUTHORIZED)

    @mock.patch.dict("os.environ", INVALID_KEYS)
    @async_test
    async def test_unauthorized_async_with(self):
        async with FieldClimateClient() as client:
            user = await client.get_user()
            self.assertDictEqual(user, UNAUTHORIZED)

    @async_test
    async def test_get_user(self):
        user = await FieldClimateClient().get_user()
        self.assertIn("username", user)

    @async_test
    async def test_get_user_async_with(self):
        async with FieldClimateClient() as client:
            user = await client.get_user()
            self.assertIn("username", user)

    @async_test
    async def test_clean_station_live(self):
        # proves usage for clean_station util.
        async with FieldClimateClient() as client:
            stations = await client.get_user_stations()
            original_station = stations[0]
            # this param can be either a station code or station dict:
            updated_stations = await asyncio.gather(
                client.get_station(original_station),
                client.get_station(original_station["name"]["original"]),
            )
            self.assertEqual(
                original_station["name"]["original"],
                updated_stations[0]["name"]["original"],
            )
            self.assertEqual(
                original_station["name"]["original"],
                updated_stations[1]["name"]["original"],
            )
