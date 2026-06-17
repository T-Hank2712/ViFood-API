from pydantic import BaseModel
from typing import Optional
    

class NameRequest(BaseModel):
    name: str