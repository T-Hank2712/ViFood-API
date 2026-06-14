from typing import Optional

from pydantic import BaseModel

from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect


class Ingredient(BaseModel):
    id: Optional[str] = None
    name: str
    description: str | None = None
    image: Optional[str] = None
    effects: list[HealthEffect] = []
    found_in: list[FoodCategory] = []
