from pydantic import BaseModel
from typing import Optional
from app.models.health_effect import HealthEffect
from app.models.food_category import FoodCategory


class CreateAdditiveRequest(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    

class UpdateAdditiveRequest(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class AdditiveDetail(BaseModel):
    id: str
    name: str
    key: str
    code: str
    description: str | None = None
    effects: list[HealthEffect] = []
    categories: list[FoodCategory] = []
