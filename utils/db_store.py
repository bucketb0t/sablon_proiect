from typing import Any, Mapping

import pymongo
from bson import ObjectId
from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.results import UpdateResult, InsertOneResult, DeleteResult


class MongoDBStore:
    '''
    Mongo database driver for general CRUD operations
    '''

    def __init__(self):
        '''
        Initializing the MongoDBStore class with a pymongo MongoCLient set on localhost:27017
        '''
        self.client = MongoClient('localhost', 27017)

    def add_document(self, db_name: str, db_collection: str, document: dict) -> InsertOneResult:
        """
        Method for adding a single document in the mongo database, specifying the database name and collection name of where the insertion to be made
        :param db_name: receives the string name of the database name to be accessed
        :param db_collection: receives the string name of the collection name to be accessed
        :param document: receives the dictionary containing the document to be added in the database and collection specified in db_name and db_collection
        :return: returns the ObjectId of the inserted document
        """
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.insert_one(document)

    def get_all_documents(self, db_name: str, db_collection: str) -> Cursor[Mapping[str, Any] | Any]:
        """
        Method for retrieving all documents inside a collection that is part of a database
        :param db_name: receives the string name of the database name to be accessed
        :param db_collection: receives the string name of the collection name to be accessed
        :return: returns a cursor containing the documents, this return needs to be stored in a variable when calling this function
        """
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.find()

    def get_document_by_id(self, db_name: str, db_collection: str, document_id: ObjectId) -> dict:
        """
        Method for retrieving the first document found in the mentioned database and collection that has the specified ObjectId
        :param db_name: receives the string name of the database name to be accessed
        :param db_collection: receives the string name of the collection name to be access
        :param document_id: receives the ObjectId for which the query will search in the mongo database
        :return: returns the document in a dictionary form of the search query made after the passed ObjectId
        """
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.find_one({"_id": document_id})

    def get_documents_by_query(self, db_name: str, db_collection: str, query: dict) -> Cursor[Mapping[str, Any] | Any]:
        """
        Method for retrieving all the documents that match the values of each key-value pair passed in the query dictionary
        :param db_name: receives the string name of the database name to be accessed
        :param db_collection: receives the string name of the collection name to be access
        :param query: receives the dictionary query after which the search is going to be made
        :return: returns all the documents it find that contain the values of each key-value pair passed in the query, this return needs to be stored in a variable when calling this function
        """
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.find(query)

    def update_document(self, db_name: str, db_collection: str, document_id: ObjectId, document: dict) -> UpdateResult:
        """
        Method for updating an existing document inside the collection of the database. This method looks up the ObjectIds inside collection and after it finds the document matching the ObjectId, then it will try to overwrite existing key-value pairs and will also add new key-value pairs that the existing document might not have had it before the update
        :param db_name: receives the string name of the database name to be accessed
        :param db_collection: receives the string name of the collection name to be access
        :param document_id: receives the ObjectId of the document you wish to update in the database
        :param document: receives the dictionary of the document that you wish to update it with
        :return: returns the UpdateResult response of the pymongo library for the update operation. You can use .modified_count method to check if the update has been made
        """
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.update_one({"_id": document_id}, {"$set": document})

    def delete_document_by_id(self, db_name: str, db_collection: str, document_id: ObjectId) -> DeleteResult:
        """
        Method for deleting a document after its ObjectId
        :param db_name: receives the string name of the database name to be accessed
        :param db_collection: receives the string name of the collection name to be access
        :param document_id: receives the ObjectId of the document you wish to delete from the database
        :return: returns the DeleteResult response of the pymongo library for the delete operation. You can use .deleted_count method to check if the deletion has been made
        """
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.delete_one({"_id": document_id})

    def delete_document_by_query(self, db_name: str, db_collection: str, query: dict) -> DeleteResult:
        """
        Method for deleting the first document whose field values matches the key values of the query dictionary
        :param db_name: receives the string name of the database name to be accessed
        :param db_collection: receives the string name of the collection name to be access
        :param query: receives the dictionary containing the key-value pairs after which the pymongo library will search in the database
        :return: returns the DeleteResult response of the pymongo library for the delete operation. You can use .deleted_count method to check if the deletion has been made
        """
        db = self.client[db_name]
        collection = db[db_collection]
        return collection.delete_one(query)

    def initialize_database(self, db_name: str, db_collection: str,
                            test_document={"name": "test_name"},
                            test_document_update={"name": "test_name_update"}):
        """
        Method that can be used to cycle a basic CRUD operation cycle on a specified collection part of a specified database
        :param db_name: receives the string name of the database name to be accessed
        :param db_collection: receives the string name of the collection name to be access
        :param test_document: receives a dictionary that can be used for basic CRD operations
        :param test_document_update: receives a dictionary that can be used for basic Update uperation
        :return: returns False if a step in initialization fails, and True if all steps in initialization pass
        """

        # Create document
        result = self.add_document(db_name, db_collection, test_document)
        test_document_id = result.inserted_id
        print(f"Document added oid: {test_document_id}")
        if not test_document_id:
            return False
        result = self.get_all_documents(db_name, db_collection)
        print(f"Documents found: {result}")
        if not result[0].get("_id") == test_document_id:
            return False

        # Read document by id
        result = None  # just to make sure there is no reference to previous step
        result = self.get_document_by_id(db_name, db_collection, test_document_id)
        print(f"Document found: {result}")
        if not result.get("_id") == test_document_id:
            return False

        # Update document
        result = None  # just to make sure there is no reference to previous step
        result = self.update_document(db_name, db_collection, test_document_id, test_document_update)
        print(f"Documents updated: {result}")
        if not result.modified_count == 1:
            return False

        # Get all documents that match the query values
        result = None  # just to make sure there is no reference to previous step
        result = self.get_documents_by_query(db_name, db_collection, test_document_update)
        print(f"Document found: {result[0]}")
        if not result[0].get("_id") == test_document_id:
            return False

        # Delete document by id
        result = None  # just to make sure there is no reference to previous step
        result = self.delete_document_by_id(db_name, db_collection, ObjectId(test_document_id))
        print(f"Document deleted: {result.deleted_count}")
        if not result.deleted_count == 1:
            return False

        # This return is True only if all previous steps pass
        return True
