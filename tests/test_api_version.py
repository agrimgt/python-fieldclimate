from unittest import TestCase

import requests


class VersionTestCase(TestCase):
    def test_version_up_to_date(self):
        # this test will fail when fieldclimate releases a new api version.
        result = requests.get("https://api.fieldclimate.com/versions.json").json()
        expected = [
            {
                "version": "1.0",
                "url": "https://api.fieldclimate.com/v1/",
                "docs": "https://api.fieldclimate.com/v1/docs/",
            }
        ]
        self.assertEqual(result, expected)
