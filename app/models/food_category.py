from pydantic import BaseModel


class FoodCategory(BaseModel):
    id: int
    name: str
