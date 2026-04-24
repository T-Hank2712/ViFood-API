from pydantic import BaseModel

class Disease(BaseModel):
    id: int
    name: str