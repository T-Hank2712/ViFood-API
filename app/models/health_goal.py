from pydantic import BaseModel
from typing import Optional


class HealthGoal(BaseModel):
    id: Optional[str] = None
    name: str
    key: Optional[str] = None
