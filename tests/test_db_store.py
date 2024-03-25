from utils.db_store import MongoDBStore
import pytest


class TestMongoDBStore:
    @pytest.fixture(scope="function")
    def mongo_driver(self):
        db = MongoDBStore()
        return db

    @pytest.fixture(scope="function")
    def sablon_document(self):
        pytest_document = {
            "name": "pytest_name"
        }
        return pytest_document

    def test_add_document(self, mongo_driver, sablon_document):
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)
        result = mongo_driver.add_document("sablon_db", "sablon_collection", sablon_document)
        print(f"Added document {result}")

        assert result.get("_id") is not None

        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

    def test_get_all_documents(self, mongo_driver, sablon_document):
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)
        result = mongo_driver.add_document("sablon_db", "sablon_collection", sablon_document)
        document_id = result.get("_id")
        result = list(mongo_driver.get_all_documents("sablon_db", "sablon_collection"))
        print(f"{result}")

        assert result[0].get("_id") == document_id
        assert result[0].get("name") == sablon_document.get("name")
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)
