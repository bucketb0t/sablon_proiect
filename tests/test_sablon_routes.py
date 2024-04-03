import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from routes.sablon_routes import router
from utils.db_store import MongoDBStore


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

    @pytest.fixture(scope="class")
    def sablon_data_bad(self):
        return {
            "name": "Test_Name_Sablon",
            "age": "twentyfour",
            "gender": "Neutral"
        }

    @pytest.fixture(scope="class")
    def sablon_db_store(self):
        return MongoDBStore()

    @pytest.fixture(scope="class")
    def sablon_data_update(self):
        return {
            "name": "Test_Name_Sablon_Update",
            "age": 42,
            "gender": "Neutral_Update"
        }

    def test_create_sablon_succes(self, sablon_router, sablon_data):
        sablon_router.request("DELETE", "/", json=sablon_data)
        response = sablon_router.post("/", json=sablon_data)
        print(f"\n\033[95mRouter: \033[92mCreate sablon success: \033[96m{response.json()}\033[0m\n")
        assert response.status_code == 200
        assert response.json().get("oid") is not None
        sablon_router.delete(f"/{response.json().get('oid')}")

    def test_create_sablon_fail(self, sablon_router, sablon_data_bad):
        sablon_router.request("DELETE", "/", json=sablon_data_bad)
        with pytest.raises(HTTPException) as exc_info:
            sablon_router.post("/", json=sablon_data_bad)
        print(f"\n\033[95mRouter: \033[92mCreate sablon fail: \033[96m{exc_info}\033[0m\n")
        assert exc_info.value.status_code == 400
        assert "Input should be a valid integer" in str(exc_info.value.detail)  # Check for the substring

    def test_get_all_sablons_succes(self, sablon_router, sablon_data):
        sablon_router.request("DELETE", "/", json=sablon_data)
        sablon_router.request("DELETE", "/", json=sablon_data)
        response = sablon_router.post("/", json=sablon_data)
        sablon_oid_1 = response.json().get("oid")
        response = sablon_router.post("/", json=sablon_data)
        sablon_oid_2 = response.json().get("oid")
        response = sablon_router.get("/")
        print(f"\n\033[95mRouter: \033[92mGet all sablons success: \033[96m{response.json()}\033[0m\n")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0] == sablon_data
        assert response.json()[1] == sablon_data
        sablon_router.delete(f"/{sablon_oid_1}")
        sablon_router.delete(f"/{sablon_oid_2}")

    def test_get_all_sablons_fail(self, sablon_router, sablon_data_bad, sablon_db_store):
        sablon_router.request("DELETE", "/", json=sablon_data_bad)
        sablon_router.request("DELETE", "/", json=sablon_data_bad)
        sablon_1 = sablon_db_store.add_document("sablon_db", "sablon_collection", sablon_data_bad)
        sablon_data_bad.pop("_id")
        sablon_2 = sablon_db_store.add_document("sablon_db", "sablon_collection", sablon_data_bad)
        sablon_data_bad.pop("_id")
        with pytest.raises(HTTPException) as exc_info:
            sablon_router.get("/")
        print(f"\n\033[95mRouter: \033[92mGet all sablons fail: \033[96m{exc_info}\033[0m\n")
        assert exc_info.value.status_code == 500
        assert "Input should be a valid integer" in str(exc_info.value.detail)  # Check for the substring
        sablon_router.delete(f"/{sablon_1.inserted_id}")
        sablon_router.delete(f"/{sablon_2.inserted_id}")

    def test_get_sablon_by_succes(self, sablon_router, sablon_data):
        sablon_router.request("DELETE", "/", json=sablon_data)
        response = sablon_router.post("/", json=sablon_data)
        sablon_oid = response.json().get("oid")

        # Get by oid
        response = sablon_router.get(f"/sabloane/{sablon_oid}")
        print(f"\n\033[95mRouter: \033[92mGet sablon by oid success: \033[96m{response.json()}\033[0m\n")
        assert response.status_code == 200
        assert response.json() == sablon_data

        # Get by query
        response = sablon_router.request("GET",f"/sabloane/{None}", json=sablon_data)
        print(f"\n\033[95mRouter: \033[92mGet sablon by query success: \033[96m{response.json()}\033[0m\n")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0] == sablon_data

        sablon_router.delete(f"/{sablon_oid}")

    def test_get_sablon_by_fail(self, sablon_router, sablon_data_bad, sablon_db_store):
        sablon_router.request("DELETE", "/", json=sablon_data_bad)
        sablon = sablon_db_store.add_document("sablon_db", "sablon_collection", sablon_data_bad)
        sablon_data_bad.pop("_id")

        # Get by oid
        with pytest.raises(HTTPException) as exc_info:
            sablon_router.get(f"/sabloane/{sablon.inserted_id}")
        print(f"\n\033[95mRouter: \033[92mGet sablon by oid fail: \033[96m{exc_info}\033[0m\n")
        assert exc_info.value.status_code == 500
        assert "Input should be a valid integer" in str(exc_info.value.detail)  # Check for the substring

        # Get by query
        with pytest.raises(HTTPException) as exc_info:
            sablon_router.request("GET",f"/sabloane/{None}", json=sablon_data_bad)
        print(f"\n\033[95mRouter: \033[92mGet sablon by query fail: \033[96m{exc_info}\033[0m\n")
        assert exc_info.value.status_code == 500
        assert "Input should be a valid integer" in str(exc_info.value.detail)  # Check for the substring

        # Get by oid AND query at the same time
        with pytest.raises(HTTPException, match="Error! Bad get request") as exc_info:
            sablon_router.request("GET",f"/sabloane/{sablon.inserted_id}", json=sablon_data_bad)
        print(f"\n\033[95mRouter: \033[92mGet sablon by oid AND query fail: \033[96m{exc_info}\033[0m\n")
        assert exc_info.value.status_code == 400
        assert "Error! Bad get request" in str(exc_info.value.detail)  # Check for the substring

        sablon_router.delete(f"/{sablon.inserted_id}")

    def test_update_sablon_success(self, sablon_router, sablon_data, sablon_data_update):
        sablon_router.request("DELETE", "/", json=sablon_data)
        sablon_router.request("DELETE", "/", json=sablon_data_update)
        response = sablon_router.post("/", json=sablon_data)
        sablon_id = response.json().get("oid")
        response = sablon_router.put(f"/{sablon_id}",json=sablon_data_update)
        print(f"\n\033[95mRouter: \033[92mUpdate sablon success: \033[96m{response.json()}\033[0m\n")
        assert response.status_code == 200
        assert response.json() == {"result": f"Documents updated: 1"}
        sablon_router.delete(f"/{sablon_id}")

    @pytest.mark.parametrize("input_case_data, expected_output", [
        ({"name": 123456}, "Error! 'name' parameter is not a string instance" ),
        ({"age": "fortytwo"}, "Error! 'age' parameter is not an integer instance"),
        ({"gender": False}, "Error! 'gender' parameter is not a string instance")
    ])
    def test_update_sablon_fail(self, sablon_router, sablon_data, input_case_data, expected_output):
        sablon_router.request("DELETE", "/", json=sablon_data)
        sablon_router.request("DELETE", "/", json=input_case_data)
        response = sablon_router.post("/", json=sablon_data)
        sablon_id = response.json().get("oid")
        with pytest.raises(HTTPException) as exc_info:
            sablon_router.put(f"/{sablon_id}", json=input_case_data)
        print(f"\n\033[95mRouter: \033[92mUpdate sablon fail: \033[96m{exc_info}\033[0m\n")
        assert exc_info.value.status_code == 400
        assert expected_output in str(exc_info.value.detail)  # Check for the substring
        sablon_router.delete(f"/{sablon_id}")

    def test_delete_sablon_by_succes(self, sablon_router, sablon_data):
        sablon_router.request("DELETE", "/", json=sablon_data)
        sablon_router.request("DELETE", "/", json=sablon_data)
        response = sablon_router.post("/", json=sablon_data)
        sablon_oid_1 = response.json().get("oid")
        response = sablon_router.post("/", json=sablon_data)
        sablon_oid_2 = response.json().get("oid")

        # Delete by oid
        response = sablon_router.delete(f"/{sablon_oid_1}")
        print(f"\n\033[95mRouter: \033[92mDelete sablon by oid success: \033[96m{response.json()}\033[0m\n")
        assert response.status_code == 200
        assert response.json() == {"result": f"Documents deleted: 1"}

        # Delete by query
        response = sablon_router.request("DELETE",f"/{None}", json=sablon_data)
        print(f"\n\033[95mRouter: \033[92mDelete sablon by query success: \033[96m{response.json()}\033[0m\n")
        assert response.status_code == 200
        assert response.json() == {"result": f"Document deleted: 1"}