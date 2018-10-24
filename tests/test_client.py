from datetime import datetime
from unittest import TestCase, mock

from fieldclimate.client import BaseClient, HmacClient
from tests.utils import async_test


class BaseClientTestCase(TestCase):
    class TestClient(BaseClient):
        base_url = "https://httpbin.org"

        def httpbin_get(self):
            return self.get("/get")

        def httpbin_post(self):
            return self.post("/post")

        def httpbin_put(self):
            return self.put("/put")

        def httpbin_delete(self):
            return self.delete("/delete")

        def httpbin_json(self):
            return self.get("/json")

    def test_httpbin_get_sync(self):
        client = self.TestClient()
        self.assertIn("args", client.httpbin_get())

    def test_httpbin_post_sync(self):
        client = self.TestClient()
        self.assertIn("args", client.httpbin_post())

    def test_httpbin_put_sync(self):
        client = self.TestClient()
        self.assertIn("args", client.httpbin_put())

    def test_httpbin_delete_sync(self):
        client = self.TestClient()
        self.assertIn("args", client.httpbin_delete())

    def test_httpbin_json_sync(self):
        client = self.TestClient()
        self.assertIn("slideshow", client.httpbin_json())

    @async_test
    async def test_httpbin_get_async(self):
        async with self.TestClient() as client:
            self.assertIn("args", await client.httpbin_get())

    @async_test
    async def test_httpbin_post_async(self):
        async with self.TestClient() as client:
            self.assertIn("args", await client.httpbin_post())

    @async_test
    async def test_httpbin_put_async(self):
        async with self.TestClient() as client:
            self.assertIn("args", await client.httpbin_put())

    @async_test
    async def test_httpbin_delete_async(self):
        async with self.TestClient() as client:
            self.assertIn("args", await client.httpbin_delete())

    @async_test
    async def test_httpbin_json_async(self):
        async with self.TestClient() as client:
            self.assertIn("slideshow", await client.httpbin_json())

    def test_incorrect_with(self):
        with self.assertRaises(TypeError):
            with self.TestClient() as client:
                pass  # pragma: no cover

    def test_no_base_url(self):
        client = self.TestClient()
        client.base_url = None
        with self.assertRaises(TypeError):
            client.httpbin_json()


class HmacClientTestCase(TestCase):
    class TestClient(HmacClient):
        base_url = "https://httpbin.org"
        settings_prefix = "TEST"
        public_key = None
        private_key = None

        def httpbin_json(self):
            return self.get("/json")

    @mock.patch("fieldclimate.client.datetime")
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
        "os.environ", {"TEST_PUBLIC_KEY": "super", "TEST_PRIVATE_KEY": "secret"}
    )
    def test_hmac_env_keys(self):
        # mock-set keys in environment
        client = self.TestClient()
        _ = client.httpbin_json()
        self.assertEqual(client.public_key, "super")
        self.assertEqual(client.private_key, "secret")

    @mock.patch("os.environ")
    def test_hmac_env_null(self, environ):
        _ = environ.pop("TEST_PUBLIC_KEY", None)
        _ = environ.pop("TEST_PRIVATE_KEY", None)
        # mock-removed keys from environment
        client = self.TestClient()
        with self.assertRaises(TypeError):
            client.httpbin_json()
