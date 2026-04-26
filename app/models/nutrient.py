from typing import List, Optional

from pydantic import BaseModel

from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect


class Nutrient(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    effects: List[HealthEffect] = []
    found_in: List[FoodCategory] = []
