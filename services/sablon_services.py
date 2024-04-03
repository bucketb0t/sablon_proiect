from bson import ObjectId

from utils.db_store import MongoDBStore
from models.sablon_model import SablonModel


class SablonServices:
    def __init__(self):
        self.db = MongoDBStore()

    def add_sablon(self, sablon_model: SablonModel) -> dict:
        try:
            result = self.db.add_document("sablon_db", "sablon_collection", sablon_model.dict())
            print(f"Sablon successfully added: {result.inserted_id}")
            return {"oid": result.inserted_id}
        except Exception as e:
            return {"error": str(e)}

    def get_all_sabloane(self) -> list[SablonModel] | dict:
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
        try:
            result = self.db.get_document_by_id("sablon_db", "sablon_collection", ObjectId(sablon_oid))
            result.pop("_id")
            return SablonModel(**result)
        except Exception as e:
            return {"error": str(e)}

    def get_sabloane_by_query(self, sablon_query: dict) -> list[SablonModel] | dict:
        try:
            results = self.db.get_documents_by_query("sablon_db", "sablon_collection", sablon_query)
            sabloane = []
            for result in results:
                sabloane.append(SablonModel(**result))
            return sabloane

        except Exception as e:
            return {"error": str(e)}

    def update_sablon(self, sablon_oid: str, sablon: dict) -> dict:
        try:
            result = self.db.update_document("sablon_db", "sablon_collection", ObjectId(sablon_oid), sablon)
            return {"result": f"Documents updated: {result.modified_count}"}
        except Exception as e:
            return {"error": str(e)}

    def delete_sablon_by_id(self, sablon_oid: str) -> dict:

        try:
            result = self.db.delete_document_by_id("sablon_db", "sablon_collection", ObjectId(sablon_oid))
            return {"result": f"Documents deleted: {result.deleted_count}"}

        except Exception as e:
            return {"error": str(e)}

    def delete_sablon_by_query(self, sablon_query: dict) -> dict:

        try:
            result = self.db.delete_document_by_query("sablon_db", "sablon_collection", sablon_query)
            return {"result": f"Document deleted: {result.deleted_count}"}

        except Exception as e:
            return {"error": str(e)}
