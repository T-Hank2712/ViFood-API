from pydantic import BaseModel
from typing import Optional


class CreateAdditiveRequest(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    

class UpdateAdditiveRequest(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
