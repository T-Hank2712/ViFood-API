from pydantic import BaseModel


class HealthEffect(BaseModel):
    id: int
    title: str
