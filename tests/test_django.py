from unittest import TestCase

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from fieldclimate.django import DjangoFieldClimateClient
from tests.utils import async_test

settings.configure(FIELDCLIMATE_PUBLIC_KEY="DJANGO", FIELDCLIMATE_PRIVATE_KEY="DANGO")


class DjangoTestCase(TestCase):
    @async_test
    async def test_settings_keys(self):
        # Ensure that public and private keys are set according to django's settings:
        client = DjangoFieldClimateClient()
        self.assertEqual(client.public_key, "DJANGO")
        self.assertEqual(client.private_key, "DANGO")

    @async_test
    async def test_unconfigured_public_key(self):
        with override_settings():
            del settings.FIELDCLIMATE_PUBLIC_KEY
            with self.assertRaises(ImproperlyConfigured):
                DjangoFieldClimateClient()

    @async_test
    async def test_unconfigured_private_key(self):
        with override_settings():
            del settings.FIELDCLIMATE_PRIVATE_KEY
            with self.assertRaises(ImproperlyConfigured):
                DjangoFieldClimateClient()
