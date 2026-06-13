from typing import Optional

from pydantic import BaseModel


class Nutrient(BaseModel):
    id: Optional[str] = None
    name: str
    key: Optional[str] = None
    description: Optional[str] = None
