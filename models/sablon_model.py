"""
This module defines a Pydantic BaseModel for representing Sablon documents.

Attributes:
    None

Classes:
    SablonModel: A Pydantic BaseModel representing Sablon documents.

"""

from pydantic import BaseModel
from typing import Optional


class SablonModel(BaseModel):
    """
    A Pydantic BaseModel representing Sablon documents.

    Attributes:
        name (str): The name of the Sablon document.
        age (Optional[int]): The age of the Sablon document (optional).
        gender (Optional[str]): The gender of the Sablon document (optional).

    """
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
