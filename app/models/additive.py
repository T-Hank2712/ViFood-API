from pydantic import BaseModel


class Additive(BaseModel):
    id: int
    name: str
    description: str | None = None
