from unittest import TestCase

import asks

from tests.utils import async_test

# TODO: This test is broken!
#  https://api.fieldclimate.com/v2/docs/ has been released but
#  https://api.fieldclimate.com/versions.json has not been updated.


async def fetch_versions():
    url = "https://api.fieldclimate.com/versions.json"
    response = await asks.get(url)
    return response.json()


class VersionTestCase(TestCase):
    @async_test
    async def test_version_up_to_date(self):
        # this test will fail when fieldclimate publishes a new api version to versions.json.
        result = await fetch_versions()
        expected = [
            {
                "version": "1.0",
                "url": "https://api.fieldclimate.com/v1/",
                "docs": "https://api.fieldclimate.com/v1/docs/",
            }
        ]
        self.assertEqual(result, expected)
