from pydantic import BaseModel
from typing import Optional


class CreateIngredientRequest(BaseModel):
    name: str
    description: Optional[str] = None
    

class UpdateIngredientRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
