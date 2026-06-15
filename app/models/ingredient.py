from typing import Optional
from pydantic import BaseModel


class Ingredient(BaseModel):
    id: Optional[str] = None
    name: str
    key: Optional[str] = None
    description: str | None = None
