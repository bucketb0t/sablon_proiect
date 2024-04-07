"""
This module provides services for managing Sablon documents in a MongoDB database.

Attributes:
    None

Classes:
    SablonServices: A class containing methods for CRUD operations on Sablon documents.

"""

from bson import ObjectId

from utils.db_store import MongoDBStore
from models.sablon_model import SablonModel


class SablonServices:
    """
       A class containing methods for CRUD operations on Sablon documents.

       Methods:
           __init__: Initializes the MongoDBStore instance.
           add_sablon: Adds a new Sablon document to the database.
           get_all_sabloane: Retrieves all Sablon documents from the database.
           get_sablon_by_oid: Retrieves a Sablon document by its ObjectId.
           get_sabloane_by_query: Retrieves Sablon documents based on a query.
           update_sablon: Updates a Sablon document.
           delete_sablon_by_id: Deletes a Sablon document by its ObjectId.
           delete_sablon_by_query: Deletes Sablon documents based on a query.
       """

    def __init__(self):
        """
       Initializes the MongoDBStore instance.

       Args:
           None

       Returns:
           None
       """
        self.db = MongoDBStore()

    def add_sablon(self, sablon_model: SablonModel) -> dict:
        """
       Adds a new Sablon document to the database.

       Args:
           sablon_model (SablonModel): The SablonModel instance to be added.

       Returns:
           Union[dict, InsertOneResult]: A dictionary containing the result of the operation or InsertOneResult object.
       """
        try:
            result = self.db.add_document("sablon_db", "sablon_collection", sablon_model.dict())
            print(f"Sablon successfully added: {result.inserted_id}")
            return {"oid": result.inserted_id}
        except Exception as e:
            return {"error": str(e)}

    def get_all_sabloane(self) -> list[SablonModel] | dict:
        """
        Retrieves all Sablon documents from the database.

        Returns:
            Union[List[SablonModel], dict]: A list of SablonModel instances or a dictionary containing the error message.
        """
        try:
            results = self.db.get_all_documents("sablon_db", "sablon_collection")
            sabloane = []
            for result in results:
                result.pop("_id")
                sabloane.append(SablonModel(**result))
            return sabloane  # Vom returna o lista de Sablon Modele
        except Exception as e:
            return {"error": str(e)}

    def get_sablon_by_oid(self, sablon_oid: str) -> SablonModel | dict:
        """
        Retrieves a Sablon document by its ObjectId.

        Args:
            sablon_oid (str): The ObjectId of the Sablon document.

        Returns:
            Union[SablonModel, dict]: The SablonModel instance or a dictionary containing the error message.
        """
        try:
            result = self.db.get_document_by_id("sablon_db", "sablon_collection", ObjectId(sablon_oid))
            result.pop("_id")
            return SablonModel(**result)
        except Exception as e:
            return {"error": str(e)}

    def get_sabloane_by_query(self, sablon_query: dict) -> list[SablonModel] | dict:
        """
       Retrieves Sablon documents based on a query.

       Args:
           sablon_query (dict): The query to filter Sablon documents.

       Returns:
           Union[List[SablonModel], dict]: A list of SablonModel instances or a dictionary containing the error message.
       """
        try:
            results = self.db.get_documents_by_query("sablon_db", "sablon_collection", sablon_query)
            sabloane = []
            for result in results:
                sabloane.append(SablonModel(**result))
            return sabloane

        except Exception as e:
            return {"error": str(e)}

    def update_sablon(self, sablon_oid: str, sablon: dict) -> dict:
        """
        Updates a Sablon document.

        Args:
            sablon_oid (str): The ObjectId of the Sablon document.
            sablon (dict): The data to update the Sablon document with.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        try:
            result = self.db.update_document("sablon_db", "sablon_collection", ObjectId(sablon_oid), sablon)
            return {"result": f"Documents updated: {result.modified_count}"}
        except Exception as e:
            return {"error": str(e)}

    def delete_sablon_by_id(self, sablon_oid: str) -> dict:
        """
        Deletes a Sablon document by its ObjectId.

        Args:
            sablon_oid (str): The ObjectId of the Sablon document.

        Returns:
            dict: A dictionary containing the result of the operation.
        """

        try:
            result = self.db.delete_document_by_id("sablon_db", "sablon_collection", ObjectId(sablon_oid))
            return {"result": f"Documents deleted: {result.deleted_count}"}

        except Exception as e:
            return {"error": str(e)}

    def delete_sablon_by_query(self, sablon_query: dict) -> dict:
        """
        Deletes Sablon documents based on a query.

        Args:
            sablon_query (dict): The query to filter Sablon documents.

        Returns:
            dict: A dictionary containing the result of the operation.
        """

        try:
            result = self.db.delete_document_by_query("sablon_db", "sablon_collection", sablon_query)
            return {"result": f"Document deleted: {result.deleted_count}"}

        except Exception as e:
            return {"error": str(e)}
