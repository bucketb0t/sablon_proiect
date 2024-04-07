"""
This module provides API endpoints for managing Sablon documents using FastAPI.

Attributes:
    None

Classes:
    None

Functions:
    create_sablon: Endpoint for creating a new Sablon document.
    get_all_sablons: Endpoint for retrieving all Sablon documents.
    get_sablon_by: Endpoint for retrieving a Sablon document by ObjectId or by query.
    update_sablon: Endpoint for updating a Sablon document.
    delete_sablon_by: Endpoint for deleting a Sablon document by ObjectId or by query.

"""

from typing import List, Dict, Any, Optional, Union
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from models.sablon_model import SablonModel
from services.sablon_services import SablonServices

router = APIRouter()
sablon_service = SablonServices()


@router.post("/", response_model=Dict[str, Any])
async def create_sablon(sablon_data: dict) -> Dict[str, Any]:
    """
  Endpoint for creating a new Sablon document.

  Args:
      sablon_data (dict): The data for creating the Sablon document.

  Returns:
      Dict[str, Any]: A dictionary containing the result of the operation.
  """
    try:
        result = sablon_service.add_sablon(SablonModel(**sablon_data))
        result["oid"] = str(result["oid"])

        if isinstance(result, dict) and result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        return result
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=Union[List[SablonModel], Dict[str, Any]])
async def get_all_sablons() -> List[SablonModel]:
    """
   Endpoint for retrieving all Sablon documents.

   Returns:
       Union[List[SablonModel], Dict[str, Any]]: A list of SablonModel instances or a dictionary containing the error message.
   """
    try:
        results = sablon_service.get_all_sabloane()

        if isinstance(results, dict) and results.get("error") is not None:
            raise HTTPException(status_code=400, detail=results.get("error"))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sabloane/{input_data}", response_model=Union[SablonModel, List[SablonModel]])
async def get_sablon_by(input_data: Optional[str] = None, body_data: Optional[Dict[str, Any]] = None) \
        -> Union[SablonModel, List[SablonModel]]:
    """
    Endpoint for retrieving a Sablon document by ObjectId or by query.

    Args:
        input_data (Optional[str]): The ObjectId or query parameter.
        body_data (Optional[Dict[str, Any]]): The query body data.

    Returns:
        Union[SablonModel, List[SablonModel]]: A SablonModel instance or a list of SablonModel instances.
    """
    if input_data == "None":
        input_data = None
    if input_data and body_data is None:
        try:
            result = sablon_service.get_sablon_by_oid(input_data)
            if isinstance(result, dict) and result.get("error") is not None:
                raise HTTPException(status_code=400, detail=result.get("error"))
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    elif input_data is None and body_data:
        try:
            results = sablon_service.get_sabloane_by_query(body_data)
            if isinstance(results, dict) and results.get("error") is not None:
                raise HTTPException(status_code=400, detail=results.get("error"))
            return results

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    else:
        raise HTTPException(status_code=400, detail="Error! Bad get request")


@router.put("/{input_data}", response_model=Dict[str, Any])
async def update_sablon(input_data: str, body_data: dict) -> Dict[str, Any]:
    """
    Endpoint for updating a Sablon document.

    Args:
        input_data (str): The ObjectId of the Sablon document.
        body_data (dict): The data to update the Sablon document with.

    Returns:
        Dict[str, Any]: A dictionary containing the result of the operation.
    """
    try:
        if "name" in body_data and not isinstance(body_data.get("name"), str):
            raise HTTPException(status_code=400, detail="Error! 'name' parameter is not a string instance")
        if "age" in body_data and not isinstance(body_data.get("age"), int):
            raise HTTPException(status_code=400, detail="Error! 'age' parameter is not an integer instance")
        if "gender" in body_data and not isinstance(body_data.get("gender"), str):
            raise HTTPException(status_code=400, detail="Error! 'gender' parameter is not a string instance")

        result = sablon_service.update_sablon(input_data, body_data)
        if isinstance(result, dict) and result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{input_data}", response_model=Dict[str, Any])
async def delete_sablon_by(input_data: Optional[str] = None, body_data: Optional[Dict[str, Any]] = None) -> Dict[
    str, Any]:
    """
    Endpoint for deleting a Sablon document by ObjectId or by query.

    Args:
        input_data (Optional[str]): The ObjectId or query parameter.
        body_data (Optional[Dict[str, Any]]): The query body data.

    Returns:
        Dict[str, Any]: A dictionary containing the result of the operation.
    """
    if input_data == "None":
        input_data = None

    if input_data and body_data is None:
        result = sablon_service.delete_sablon_by_id(input_data)
        if isinstance(result, dict) and result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        return result

    elif input_data is None and body_data:
        result = sablon_service.delete_sablon_by_query(body_data)
        if isinstance(result, dict) and result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        return result

    else:
        raise HTTPException(status_code=400,
                            detail="Invalid request. Please provide either an ID in the URL path or a JSON body.")
