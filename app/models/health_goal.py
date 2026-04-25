from pydantic import BaseModel


class HealthGoal(BaseModel):
    id: int
    name: str
