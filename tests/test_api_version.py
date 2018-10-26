import asyncio
from unittest import TestCase

import aiohttp


async def fetch_versions():
    url = "https://api.fieldclimate.com/versions.json"
    async with aiohttp.request("get", url) as response:
        return await response.json()


class VersionTestCase(TestCase):
    def test_version_up_to_date(self):
        # this test will fail when fieldclimate releases a new api version.
        result = asyncio.get_event_loop().run_until_complete(fetch_versions())
        expected = [
            {
                "version": "1.0",
                "url": "https://api.fieldclimate.com/v1/",
                "docs": "https://api.fieldclimate.com/v1/docs/",
            }
        ]
        self.assertEqual(result, expected)
