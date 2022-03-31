"""
Fixtures are not compatible with unittest.TestCase
"""
from fastapi.testclient import TestClient
from fastapi_testing import app


class SyncTestSimpleRequest:
    # NOTE: Removed unittest.TestCase due to a conflict with pytest
    test_client = TestClient(app.main.app)


    def test_sync_request(self, tests_setup_and_teardown):
        response = self.test_client.post("/services/login/access-token", data={
            "username": "test_user@test.com", "password": "test_password"}
                                        )
        assert response.status_code == 200
        assert "access_token" in response.json().keys()
        assert response.json().get("token_type") == "bearer"
