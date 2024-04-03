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
        print(f"\n\033[93mService: \033[92mAdd sablon success: \033[96m{result}\033[0m\n")
        assert result.get("oid") is not None
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_add_sablon_fail(self, sablon_services, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_dict)
        print(f"\n\033[93mService: \033[92mAdd sablon fail: \033[96m{result}\033[0m\n")
        assert result.get("error") is not None
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_get_all_sabloane_success(self, sablon_services, sablon_dict, sablon_model):
        for i in range(0, 3):
            sablon_services.delete_sablon_by_query(sablon_dict)

        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.add_sablon(sablon_model)

        results = sablon_services.get_all_sabloane()
        print(f"\n\033[93mService: \033[92mGet all sabloane success: \033[96m{results}\033[0m\n")
        assert len(results) == 3
        for result in results:
            assert result == sablon_model
        for result in results:
            sablon_services.delete_sablon_by_query(result.dict())

    def test_get_all_sabloane_fail(self, sablon_services, sablon_db_store, sablon_dict_bad):
        sablon_services.delete_sablon_by_query(sablon_dict_bad)

        result = sablon_db_store.add_document("sablon_db", "sablon_collection", sablon_dict_bad)
        result = sablon_services.get_all_sabloane()
        print(f"\n\033[93mService: \033[92mGet all sabloane fail: \033[96m{result}\033[0m\n")
        assert result.get("error") is not None
        sablon_services.delete_sablon_by_query(sablon_dict_bad)

    def test_get_sablon_by_oid_success(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.get_sablon_by_oid(result.get("oid"))
        print(f"\n\033[93mService: \033[92mGet sablon by oid success: \033[96m{result}\033[0m\n")
        assert result == sablon_model
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_get_sablon_by_oid_fail(self, sablon_services, sablon_db_store, sablon_dict_bad):
        sablon_services.delete_sablon_by_query(sablon_dict_bad)

        result = sablon_db_store.add_document("sablon_db", "sablon_collection", sablon_dict_bad)
        result = sablon_services.get_sablon_by_oid(result.inserted_id)
        print(f"\n\033[93mService: \033[92mGet sablon by oid fail: \033[96m{result}\033[0m\n")
        assert result.get("error") is not None
        sablon_services.delete_sablon_by_query(sablon_dict_bad)

    def test_get_sabloane_by_query_success(self, sablon_services, sablon_model, sablon_dict):

        for i in range(0, 3):
            sablon_services.delete_sablon_by_query(sablon_dict)

        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.add_sablon(sablon_model)

        results = sablon_services.get_sabloane_by_query({"age": 24})
        print(f"\n\033[93mService: \033[92mGet sabloane by query success: \033[96m{results}\033[0m\n")
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
        print(f"\n\033[93mService: \033[92mGet sabloane by query fail: \033[96m{result}\033[0m\n")
        assert result.get("error") is not None

        sablon_services.delete_sablon_by_query(sablon_dict_bad)

    def test_update_sablon_success(self, sablon_services, sablon_model, sablon_dict, sablon_dict_update):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.update_sablon(result.get("oid"), sablon_dict_update)
        print(f"\n\033[93mService: \033[92mUpdate sablon success: \033[96m{result}\033[0m\n")
        assert result == {"result": "Documents updated: 1"}

        sablon_services.delete_sablon_by_query(sablon_dict_update)

    def test_update_sablon_fail(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.update_sablon(result.get("oid"), sablon_model)
        print(f"\n\033[93mService: \033[92mUpdate sablon fail: \033[96m{result}\033[0m\n")
        assert result.get("error") is not None

    def test_delete_sablon_by_id_success(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.delete_sablon_by_id(result.get("oid"))
        print(f"\n\033[93mService: \033[92mDelete sablon by id success: \033[96m{result}\033[0m\n")
        assert result == {"result": f"Documents deleted: 1"}
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_delete_sablon_by_id_fail(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.delete_sablon_by_id(sablon_model)
        print(f"\n\033[93mService: \033[92mDelete sablon by id fail: \033[96m{result}\033[0m\n")
        assert result.get("error") is not None
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_delete_sablon_by_query_success(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.delete_sablon_by_query({"gender": "Neutral"})
        print(f"\n\033[93mService: \033[92mDelete sablon by query success: \033[96m{result}\033[0m\n")
        assert result == {"result": "Document deleted: 1"}
        sablon_services.delete_sablon_by_query(sablon_dict)

    def test_delete_sablon_by_query_fail(self, sablon_services, sablon_model, sablon_dict):
        sablon_services.delete_sablon_by_query(sablon_dict)
        result = sablon_services.add_sablon(sablon_model)
        result = sablon_services.delete_sablon_by_query(sablon_model)
        print(f"\n\033[93mService: \033[92mDelete sablon by query fail: \033[96m{result}\033[0m\n")
        assert result.get("error") is not None
        sablon_services.delete_sablon_by_query(sablon_dict)
