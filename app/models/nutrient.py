from pydantic import BaseModel


class Nutrient(BaseModel):
    id: int
    name: str
    description: str | None = None
