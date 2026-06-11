from pydantic import BaseModel


class HealthGoalRequest(BaseModel):
    name: str
