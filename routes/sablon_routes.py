from typing import List, Dict, Any, Optional, Union
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from models.sablon_model import SablonModel
from services.sablon_services import SablonServices

router = APIRouter()
sablon_service = SablonServices()


@router.post("/", response_model=Dict[str, Any])
async def create_sablon(sablon_data: dict) -> Dict[str, Any]:
    try:
        result = sablon_service.add_sablon(SablonModel(**sablon_data))
        result["oid"] = str(result["oid"])

        if isinstance(result, dict) and result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        else:
            return result
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=Union[List[SablonModel], Dict[str, Any]])
async def get_all_sablons() -> List[SablonModel]:
    try:
        results = sablon_service.get_all_sabloane()

        if isinstance(results, dict) and results.get("error") is not None:
            raise HTTPException(status_code=400, detail=results.get("error"))
        else:
            return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sabloane/{input_data}", response_model=Union[SablonModel, List[SablonModel]])
async def get_sablon_by(input_data: Optional[str] = None, body_data: Optional[Dict[str, Any]] = None) \
        -> Union[SablonModel, List[SablonModel]]:
    if input_data == "None":
        input_data = None
    if input_data and body_data is None:
        try:
            result = sablon_service.get_sablon_by_oid(input_data)
            if isinstance(result, dict) and result.get("error") is not None:
                raise HTTPException(status_code=400, detail=result.get("error"))
            else:
                return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    elif input_data is None and body_data:
        try:
            results = sablon_service.get_sabloane_by_query(body_data)
            if isinstance(results, dict) and results.get("error") is not None:
                raise HTTPException(status_code=400, detail=results.get("error"))
            else:
                return results

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    else:
        raise HTTPException(status_code=400, detail="Error! Bad get request")


@router.put("/{input_data}", response_model=Dict[str, Any])
async def update_sablon(input_data: str, body_data: dict) -> Dict[str, Any]:
    try:
        if "name" in body_data and not isinstance(body_data.get("name"),str):
            raise HTTPException(status_code=400, detail="Error! 'name' parameter is not a string instance")
        if "age" in body_data and not isinstance(body_data.get("age"), int):
            raise HTTPException(status_code=400, detail="Error! 'age' parameter is not an integer instance")
        if "gender" in body_data and not isinstance(body_data.get("gender"), str):
            raise HTTPException(status_code=400, detail="Error! 'gender' parameter is not a string instance")

        result = sablon_service.update_sablon(input_data, body_data)
        if isinstance(result, dict) and result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        else:
            return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{input_data}", response_model=Dict[str, Any])
async def delete_sablon_by(input_data: Optional[str] = None, body_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if input_data == "None":
        input_data = None

    if input_data and body_data is None:
        result = sablon_service.delete_sablon_by_id(input_data)
        if isinstance(result, dict) and result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        else:
            return result

    elif input_data is None and body_data:
        result = sablon_service.delete_sablon_by_query(body_data)
        if isinstance(result, dict) and result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        else:
            return result

    else:
        raise HTTPException(status_code=400, detail="Invalid request. Please provide either an ID in the URL path or a JSON body.")