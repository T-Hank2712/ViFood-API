from pydantic import BaseModel
from typing import Optional


class Allergy(BaseModel):
    id: Optional[str] = None
    name: str
    key: Optional[str] = None
