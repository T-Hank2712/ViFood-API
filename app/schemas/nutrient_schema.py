from pydantic import BaseModel
from typing import Optional


class CreateNutrientRequest(BaseModel):
    name: str
    description: Optional[str] = None
    

class UpdateNutrientRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
