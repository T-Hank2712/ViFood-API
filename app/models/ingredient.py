from pydantic import BaseModel


class Ingredient(BaseModel):
    id: int
    name: str
    description: str | None = None
