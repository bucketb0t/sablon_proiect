import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from routes.sablon_routes import router


class TestSablonRoutes:
    @pytest.fixture(scope="class")
    def sablon_router(self):
        return TestClient(router)

    @pytest.fixture(scope="class")
    def sablon_data(self):
        return {
            "name": "Test_Name_Sablon",
            "age": 24,
            "gender": "Neutral"
        }

    def test_create_sablon(self, sablon_router, sablon_data):
        sablon_router.request("DELETE", "/", json=sablon_data)
        response = sablon_router.post("/", json=sablon_data)
        assert response.status_code == 200
        assert response.json().get("oid") is not None
        sablon_router.delete(f"/{response.json().get('oid')}")