from pydantic import BaseModel
from typing import Optional


class SablonModel(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
