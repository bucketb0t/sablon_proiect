from typing import List, Union
from fastapi import APIRouter, HTTPException

from models.sablon_model import SablonModel
from services.sablon_services import SablonServices

router = APIRouter()
sablon_service = SablonServices()


@router.post("/", response_model=dict)
async def create_sablon(sablon_data: dict) -> dict | HTTPException:
    try:
        result = sablon_service.add_sablon(SablonModel(**sablon_data))
        result["oid"] = str(result["oid"])

        if result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        else:
            return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list)
async def get_all_sablons() -> list[SablonModel] | HTTPException:
    try:
        results = sablon_service.get_all_sabloane()

        if results.get("error") is not None:
            raise HTTPException(status_code=400, detail=results.get("error"))
        else:
            return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{input_data}", response_model=list)
async def get_sablon_by(input_data: str | None, body_data: dict | None) \
        -> list[SablonModel] | SablonModel | HTTPException:
    if input_data and body_data is None:
        try:
            result = sablon_service.get_sablon_by_oid(input_data)
            if result.get("error") is not None:
                raise HTTPException(status_code=400, detail=result.get("error"))
            else:
                return result

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    elif input_data is None and body_data:
        try:
            results = sablon_service.get_sabloane_by_query(body_data)
            if results.get("error") is not None:
                raise HTTPException(status_code=400, detail=results.get("error"))
            else:
                return results

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    else:
        raise HTTPException(status_code=400, detail="Error! Bad get request")


@router.put("/{input_data}", response_model=dict)
async def update_sablon(input_data: str, body_data: dict) -> dict | HTTPException:
    try:
        result = sablon_service.update_sablon(input_data, body_data)
        if result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        else:
            return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{input_data}", response_model=dict)
async def delete_sablon_by(input_data: str | None ,body_data: dict | None) -> dict | HTTPException:
    if input_data and body_data is None:
        result = sablon_service.delete_sablon_by_id(input_data)
        if result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        else:
            return result

    elif input_data is None and body_data:
        print("AICI")
        result = sablon_service.delete_sablon_by_query(body_data)
        if result.get("error") is not None:
            raise HTTPException(status_code=400, detail=result.get("error"))
        else:
            return result

    else:
        raise HTTPException(status_code=400, detail="Error! Bad get request")