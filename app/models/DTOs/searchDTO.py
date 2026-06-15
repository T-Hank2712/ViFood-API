from pydantic import BaseModel
from app.models.health_effect import HealthEffect
from app.models.food_category import FoodCategory


class searchDTO(BaseModel):
    id: str
    name: str
    key: str
    code: str | None = None
    description: str | None = None
    type: str
    

class searchDtoDetail(BaseModel):
    id: str
    name: str
    key: str
    code: str | None = None
    description: str | None = None
    effects: list[HealthEffect] = []
    categories: list[FoodCategory] = []
