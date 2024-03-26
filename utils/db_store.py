from typing import Any, Mapping

import pymongo
from bson import ObjectId
from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.results import UpdateResult


class MongoDBStore:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)

    def add_document(self, db_name: str, db_collection: str, document: dict) -> dict:
        db = self.client[db_name]
        collection = db[db_collection]
        collection.insert_one(document)
        return document

    def get_all_documents(self, db_name: str, db_collection: str) -> Cursor[Mapping[str, Any] | Any]:
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.find()

    def get_document_by_id(self, db_name: str, db_collection: str, document_id: ObjectId) -> dict:
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.find_one({"_id": document_id})

    def get_documents_by_query(self, db_name: str, db_collection: str, query: dict) -> Cursor[Mapping[str, Any] | Any]:
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.find(query)

    def update_document(self, db_name: str, db_collection: str, document_id: ObjectId, document: dict) -> UpdateResult:
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.update_one({"_id": document_id}, {"$set": document})

    def delete_document_by_id(self, db_name: str, db_collection: str, document_id: ObjectId):
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.delete_one({"_id": document_id})

    def delete_document_by_query(self, db_name: str, db_collection: str, query: dict):
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.delete_one(query)

    def initialize_database(self, db_name: str, db_collection: str,
                            test_document={"name": "test_name"},
                            test_document_update={"name": "test_name_update"}):
        '''

        :param db_name:
        :param db_collection:
        :param test_document:
        :param test_document_update:
        :return: False if a step in initialization fails, and True if all steps in initialization pass
        '''

        result = self.add_document(db_name, db_collection, test_document)
        test_document_id = result.get("_id")
        print(f"Document added oid: {test_document_id}")
        if not test_document_id:
            return False
        result = self.get_all_documents(db_name, db_collection)
        print(f"Documents found: {result}")
        if not result[0].get("_id") == test_document_id:
            return False

        result = None # just to make sure there is no reference to previous step
        result = self.get_document_by_id(db_name, db_collection, test_document_id)
        print(f"Document found: {result}")
        if not result.get("_id") == test_document_id:
            return False

        result = None # just to make sure there is no reference to previous step
        result = self.update_document(db_name, db_collection, test_document_id, test_document_update)
        print(f"Documents updated: {result}")
        if not result.modified_count == 1:
            return False

        result = None # just to make sure there is no reference to previous step
        result = self.get_documents_by_query(db_name, db_collection, test_document_update)
        print(f"Document found: {result[0]}")
        if not result[0].get("_id") == test_document_id:
            return False

        result = None # just to make sure there is no reference to previous step
        result = self.delete_document_by_id(db_name, db_collection, ObjectId(test_document_id))
        print(f"Document deleted: {result.deleted_count}")
        if not result.deleted_count == 1:
            return False

        # This return is True only if all previous steps pass
        return True
