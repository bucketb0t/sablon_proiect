import pytest

from utils.db_store import MongoDBStore
from services.sablon_services import SablonServices
from models.sablon_model import SablonModel


class TestSablonServices:
    @pytest.fixture(scope="class")
    def sablon_services(self):
        return SablonServices()

    @pytest.fixture(scope="class")
    def sablon_dict(self):
        return {
            "name": "Test_Name_Sablon",
            "age": 24,
            "gender": "Neutral"
        }

    @pytest.fixture(scope="class")
    def sablon_model(self, sablon_dict):
        return SablonModel(**sablon_dict)

    @pytest.fixture(scope="class")
    def sablon_dict_bad(self):
        return {
            "name": "Test_Name_Sablon_Bad",
            "age": "24",
            "gender": False,
            "place_of_birth": "Slobozia"
        }

    @pytest.fixture(scope="class")
    def sablon_db_store(self):
        return MongoDBStore()

    @pytest.fixture(scope="class")
    def sablon_dict_update(self):
        return {
            "name": "Test_Name_Sablon_Update",
            "age": 9000 + 1,
            "gender": "Neutral_Update"
        }

    def test_add_sablon_success(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        assert result.get("oid") is not None
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_add_sablon_fail(self, sablon_services, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_dict)
        print(f"result: {result}")
        assert result.get("error") is not None
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_get_all_sabloane_success(self, sablon_services, sablon_dict, sablon_model):
        for i in range(0, 3):
            sablon_services.delete_sablon_by_query(sablon_dict)

        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.add_sablon(sablon_model)

        results = sablon_services.get_all_sabloane()
        assert len(results) == 3
        for result in results:
            assert result == sablon_model
        for result in results:
            sablon_services.delete_sablon_by_query(result.dict())

    def test_get_all_sabloane_fail(self, sablon_services, sablon_db_store, sablon_dict_bad):
        sablon_services.delete_sablon_by_query(sablon_dict_bad)

        result = sablon_db_store.add_document("sablon_db", "sablon_collection", sablon_dict_bad)
        result = sablon_services.get_all_sabloane()

        assert result.get("error") is not None

        sablon_services.delete_sablon_by_query(sablon_dict_bad)

    def test_get_sablon_by_oid_success(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.get_sablon_by_oid(result.get("oid"))
        assert result == sablon_model
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_get_sablon_by_oid_fail(self, sablon_services, sablon_db_store, sablon_dict_bad):
        sablon_services.delete_sablon_by_query(sablon_dict_bad)

        result = sablon_db_store.add_document("sablon_db", "sablon_collection", sablon_dict_bad)
        result = sablon_services.get_sablon_by_oid(result.inserted_id)

        assert result.get("error") is not None

        sablon_services.delete_sablon_by_query(sablon_dict_bad)

    def test_get_sabloane_by_query_success(self, sablon_services, sablon_model, sablon_dict):

        for i in range(0, 3):
            sablon_services.delete_sablon_by_query(sablon_dict)

        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.add_sablon(sablon_model)

        results = sablon_services.get_sabloane_by_query({"age": 24})
        for result in results:
            assert result.age == sablon_dict.get("age")

        # ALTFEL
        # result = sablon_services.get_sabloane_by_query(sablon_dict)
        # for result in results:
        #   assert result == sablon_model

        for result in results:
            sablon_services.delete_sablon_by_query(result.dict())

    def test_get_sabloane_by_query_fail(self, sablon_services, sablon_db_store, sablon_dict_bad):
        sablon_services.delete_sablon_by_query(sablon_dict_bad)

        result = sablon_db_store.add_document("sablon_db", "sablon_collection", sablon_dict_bad)
        result = sablon_services.get_sabloane_by_query({"age": "24"})

        assert result.get("error") is not None

        sablon_services.delete_sablon_by_query(sablon_dict_bad)

    def test_update_sablon_success(self, sablon_services, sablon_model, sablon_dict, sablon_dict_update):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.update_sablon(result.get("oid"), sablon_dict_update)
        # print(f"result: {result}")
        assert result == {"result": "Documents updated: 1"}

        sablon_services.delete_sablon_by_query(sablon_dict_update)

    def test_update_sablon_fail(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.update_sablon(result.get("oid"), sablon_model)
        # print(f"result: {result}")
        assert result.get("error") is not None

    def test_delete_sablon_by_id_success(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.delete_sablon_by_id(result.get("oid"))
        assert result == {"result": f"Documents deleted: 1"}
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_delete_sablon_by_id_fail(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.delete_sablon_by_id(sablon_model)
        assert result.get("error") is not None
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_delete_sablon_by_query_success(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.delete_sablon_by_query({"gender": "Neutral"})
        assert result == {"result": "Document deleted: 1"}
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_delete_sablon_by_query_fail(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.delete_sablon_by_query(sablon_model)
        assert result.get("error") is not None
        sablon_services.delete_sablon_by_query(sablon_dict)
