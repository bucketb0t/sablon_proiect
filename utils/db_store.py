import pymongo
from bson import ObjectId
from pymongo import MongoClient


class MongoDBStore:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)

    def add_document(self, db_name: str, db_collection: str, document: dict):
        db = self.client[db_name]
        collection = db[db_collection]
        collection.insert_one(document)
        return document

    def get_all_documents(self, db_name: str, db_collection: str):
        db = self.client[db_name]
        collection = db[db_collection]
        return collection

    def get_document_by_id(self, db_name: str, db_collection: str, document_id: str):
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.find_one({"_id": ObjectId(document_id)})

    def get_documents_by_query(self, db_name: str, db_collection: str, query: dict):
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.find(query)

    def update_document(self, db_name: str, db_collection: str, document_id: str, document: dict):
        db = self.client[db_name]
        collection = db[db_collection]
        collection.update_one({"_id": ObjectId(document_id)}, {"$set": document})
        return document

    def delete_document(self, db_name: str, db_collection: str, document_id: str):
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.delete_one({"_id": ObjectId(document_id)})

    def initialize_database(self, db_name: str, db_collection: str):
        db = self.client[db_name]
        collection = db[db_collection]

        test_document = {
            "name": "test_name"
        }
        test_document_update = {
            "name": "test_name_update"
        }
        result = self.add_document(db_name, db_collection, test_document)
        test_document_id = str(result.inserted_id)
        print(f"Document added oid: {test_document_id}")
        result = self.get_all_documents(db_name, db_collection)
        print(f"Documents found: {result}")
        result = self.get_document_by_id(db_name, db_collection, test_document_id)
        print(f"Document found: {result}")
        result = self.update_document(db_name, db_collection, test_document_id, test_document_update)
        print(f"Documents updated: {result.modified_count}")
        result = self.get_documents_by_query(db_name, db_collection, test_document_update)
        print(f"Document found: {result}")
        result = self.delete_document(db_name, db_collection, test_document_id)
        print(f"Document deleted: {result.deleted_count}")
