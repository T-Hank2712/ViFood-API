from typing import Optional
from pydantic import BaseModel


class Additive(BaseModel):
    id: Optional[str] = None
    name: str
    key: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
