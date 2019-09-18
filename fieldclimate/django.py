from django.conf import settings

from fieldclimate import FieldClimateClient


class DjangoFieldClimateClient(FieldClimateClient):
    """Look for HMAC keys in Django's settings first."""

    @classmethod
    def find_public_key(cls):
        try:
            return settings.FIELDCLIMATE_PUBLIC_KEY
        except AttributeError:
            return super(DjangoFieldClimateClient, cls).find_public_key()

    @classmethod
    def find_private_key(cls):
        try:
            return settings.FIELDCLIMATE_PRIVATE_KEY
        except AttributeError:
            return super(DjangoFieldClimateClient, cls).find_private_key()
