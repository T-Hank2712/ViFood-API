from typing import List, Optional

from pydantic import BaseModel


class Nutrient(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    effects: List[str] = []
    found_in: List[str] = []
