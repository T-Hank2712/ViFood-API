from pydantic import BaseModel
from typing import Optional


class HealthEffect(BaseModel):
    id: Optional[str] = None
    name: str
    key: Optional[str] = None
    description: Optional[str] = None
