from datetime import datetime
from unittest import TestCase, mock

from fieldclimate import FieldClimateClient
from tests.utils import async_test


class ClientTestCase(TestCase):
    class TestClient(FieldClimateClient):
        base_location = "https://httpbin.org"

        async def httpbin_get(self):
            return (await self.get(path="/get")).json()

        async def httpbin_post(self):
            return (await self.post(path="/post")).json()

        async def httpbin_put(self):
            return (await self.put(path="/put")).json()

        async def httpbin_delete(self):
            return (await self.delete(path="/delete")).json()

        async def httpbin_json(self):
            return (await self.get(path="/json")).json()

    @async_test
    async def test_httpbin_get(self):
        client = self.TestClient()
        self.assertIn("args", await client.httpbin_get())

    @async_test
    async def test_httpbin_post(self):
        client = self.TestClient()
        self.assertIn("args", await client.httpbin_post())

    @async_test
    async def test_httpbin_put(self):
        client = self.TestClient()
        self.assertIn("args", await client.httpbin_put())

    @async_test
    async def test_httpbin_delete(self):
        client = self.TestClient()
        self.assertIn("args", await client.httpbin_delete())

    @async_test
    async def test_httpbin_json(self):
        client = self.TestClient()
        self.assertIn("slideshow", await client.httpbin_json())

    @async_test
    async def test_httpbin_get_async_with(self):
        async with self.TestClient() as client:
            self.assertIn("args", await client.httpbin_get())

    @async_test
    async def test_httpbin_post_async_with(self):
        async with self.TestClient() as client:
            self.assertIn("args", await client.httpbin_post())

    @async_test
    async def test_httpbin_put_async_with(self):
        async with self.TestClient() as client:
            self.assertIn("args", await client.httpbin_put())

    @async_test
    async def test_httpbin_delete_async_with(self):
        async with self.TestClient() as client:
            self.assertIn("args", await client.httpbin_delete())

    @async_test
    async def test_httpbin_json_async_with(self):
        async with self.TestClient() as client:
            self.assertIn("slideshow", await client.httpbin_json())

    @mock.patch("fieldclimate.datetime")
    def test_hmac_headers(self, mock_datetime):
        mock_datetime.utcnow = mock.Mock(
            return_value=datetime(2018, 10, 22, 22, 22, 22, 222222)
        )
        client = self.TestClient(public_key="super", private_key="secret")
        self.assertDictEqual(
            client.get_headers("GET", "/route"),
            {
                "Accept": "application/json",
                "Date": "Mon, 22 Oct 2018 22:22:22 GMT",
                "Authorization": "hmac super:ad202a3c38834bb3b53697ea8df5cc4b342264619986d9786c0b9363d94ecabf",
            },
        )
        # these keys were set in __init__:
        self.assertEqual(client.public_key, "super")
        self.assertEqual(client.private_key, "secret")

    @mock.patch.dict(
        "os.environ",
        {"FIELDCLIMATE_PUBLIC_KEY": "super", "FIELDCLIMATE_PRIVATE_KEY": "secret"},
    )
    @async_test
    async def test_hmac_env_keys(self):
        # keys are now mock-set in environment
        client = self.TestClient()
        self.assertEqual(client.public_key, "super")
        self.assertEqual(client.private_key, "secret")

    @mock.patch("os.environ")
    @async_test
    async def test_hmac_null_keys(self, environ):
        _ = environ.pop("FIELDCLIMATE_PUBLIC_KEY", None)
        _ = environ.pop("FIELDCLIMATE_PRIVATE_KEY", None)
        # keys are now mock-removed from environment
        client = self.TestClient()
        with self.assertRaises(TypeError):
            await client.httpbin_json()
