from pydantic import BaseModel
from typing import Optional
from app.models.health_effect import HealthEffect
from app.models.food_category import FoodCategory


class CreateIngredientRequest(BaseModel):
    name: str
    description: Optional[str] = None
    

class UpdateIngredientRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class IngredientDetail(BaseModel):
    id: str
    name: str
    key: str
    description: str | None = None
    effects: list[HealthEffect] = []
    categories: list[FoodCategory] = []
