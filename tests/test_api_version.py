import asyncio
from unittest import TestCase

import asks

# TODO: This test is broken!
#  https://api.fieldclimate.com/v2/docs/ has been released but
#  https://api.fieldclimate.com/versions.json has not been updated.


async def fetch_versions():
    url = "https://api.fieldclimate.com/versions.json"
    response = await asks.get(url)
    return response.json()


class VersionTestCase(TestCase):
    def test_version_up_to_date(self):
        # this test will fail when fieldclimate publishes a new api version to versions.json.
        result = asyncio.get_event_loop().run_until_complete(fetch_versions())
        expected = [
            {
                "version": "1.0",
                "url": "https://api.fieldclimate.com/v1/",
                "docs": "https://api.fieldclimate.com/v1/docs/",
            }
        ]
        self.assertEqual(result, expected)
