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

    @pytest.fixture(scope="function")
    def sablon_document_update(self):
        pytest_document = {
            "name": "pytest_name_update",
            "age": 65,
            "active": False
        }
        return pytest_document

    def test_add_document(self, mongo_driver, sablon_document):
        # Clean db from previous run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

        # Create document
        result = mongo_driver.add_document("sablon_db", "sablon_collection", sablon_document)
        print(f"\n\033[91mUtils: \033[92mAdd document: \033[96mAdded document {result.inserted_id}\033[0m\n")

        assert result.inserted_id is not None

        # Clean db after successful test run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

    def test_get_all_documents(self, mongo_driver, sablon_document):
        # Clean db from previous run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

        # Create document
        result = mongo_driver.add_document("sablon_db", "sablon_collection", sablon_document)

        # Store created document Objectid
        document_id = result.inserted_id

        # Get all documents
        result = list(mongo_driver.get_all_documents("sablon_db", "sablon_collection"))
        print(f"\n\033[91mUtils: \033[92mGet all documents: \033[96m{result}\033[0m\n")

        assert result[0].get("_id") == document_id
        assert result[0].get("name") == sablon_document.get("name")

        # Clean db after successful test run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

    def test_get_document_by_id(self, mongo_driver, sablon_document):
        # Clean db from previous run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

        # Create document
        result = mongo_driver.add_document("sablon_db", "sablon_collection", sablon_document)

        # Store created document Objectid
        document_id = result.inserted_id

        # Get document by id
        result = mongo_driver.get_document_by_id("sablon_db", "sablon_collection", document_id)
        print(f"\n\033[91mUtils: \033[92mGet document by id: \033[96m{result}\033[0m\n")

        assert result.get("_id") == document_id
        assert result.get("name") == sablon_document.get("name")

        # Clean db after successful test run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

    def test_get_documents_by_query(self, mongo_driver, sablon_document):
        # Clean db from previous run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

        # Create document
        result = mongo_driver.add_document("sablon_db", "sablon_collection", sablon_document)

        # Store created document Objectid
        document_id = result.inserted_id

        # Get documents by query
        result = mongo_driver.get_documents_by_query("sablon_db", "sablon_collection", {"name": sablon_document.get("name")})
        print(f"\n\033[91mUtils: \033[92mGet documents by query: \033[96m{result}\033[0m\n")

        assert result[0].get("_id") == document_id
        assert result[0].get("name") == sablon_document.get("name")

        # Clean db after successful test run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

    def test_update_document(self, mongo_driver, sablon_document, sablon_document_update):
        # Clean db from previous run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document_update)

        # Create document
        result = mongo_driver.add_document("sablon_db", "sablon_collection", sablon_document)

        # Store created document Objectid
        document_id = result.inserted_id

        # Update document
        result = mongo_driver.update_document("sablon_db", "sablon_collection", document_id, sablon_document_update)
        print(f"\n\033[91mUtils: \033[92mUpdate document: \033[96mUpdated document {result.modified_count}\033[0m\n")

        assert result.modified_count == 1

        # Get documents by query
        result = mongo_driver.get_document_by_id("sablon_db", "sablon_collection", document_id)

        assert result.get("_id") == document_id
        assert result.get("name") == sablon_document_update.get("name")
        assert result.get("age") == sablon_document_update.get("age")
        assert result.get("active") == sablon_document_update.get("active")

        # Clean db after successful test run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document_update)

    def test_delete_document_by_id(self, mongo_driver, sablon_document):
        # Clean db from previous run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

        # Create document
        result = mongo_driver.add_document("sablon_db", "sablon_collection", sablon_document)

        # Store created document Objectid
        document_id = result.inserted_id

        # Delete document by id
        result = mongo_driver.delete_document_by_id("sablon_db", "sablon_collection", document_id)
        print(f"\n\033[91mUtils: \033[92mDelete document document by id: \033[96mDeleted document {result.deleted_count}\033[0m\n")

        assert result.deleted_count == 1

        # Clean db after successful test run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

    def test_delete_document_by_query(self, mongo_driver, sablon_document):
        # Clean db from previous run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

        # Create document
        result = mongo_driver.add_document("sablon_db", "sablon_collection", sablon_document)

        # Store created document Objectid
        document_id = result.inserted_id

        # Delete document by id
        result = mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", {"name": sablon_document.get("name")})
        print(f"\n\033[91mUtils: \033[92mDelete document document by query: \033[96mDeleted document {result.deleted_count}\033[0m\n")

        assert result.deleted_count == 1

        # Clean db after successful test run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)

    def test_initialize_database(self, mongo_driver, sablon_document, sablon_document_update):
        # Clean db from previous run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document_update)

        # Run initialize_database function and store the return
        result = mongo_driver.initialize_database("sablon_db", "sablon_collection", sablon_document, sablon_document_update)
        print(f"\n\033[91mUtils: \033[92mInitialize database: \033[96m{result}\033[0m\n")

        assert result is True

        # Clean db after successful test run
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document)
        mongo_driver.delete_document_by_query("sablon_db", "sablon_collection", sablon_document_update)
