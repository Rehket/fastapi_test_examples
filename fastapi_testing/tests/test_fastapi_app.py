from fastapi.testclient import TestClient
from fastapi_testing import app
import pytest
import unittest



client = TestClient(app.main.app)

class AsyncTestSimpleRequest(unittest.IsolatedAsyncioTestCase):

    @pytest.mark.asyncio
    async def test_asyncio_request(self):
        response = client.get("/services/health")
        assert response.status_code == 200
        assert response.json() == {"health": "ok"}

class SyncTestSimpleRequest(unittest.TestCase):

     def test_sync_request(self):
        response = client.get("/services/health")
        assert response.status_code == 200
        assert response.json() == {"health": "ok"}
