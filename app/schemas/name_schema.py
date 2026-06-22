from pydantic import BaseModel
    

class NameRequest(BaseModel):
    name: str
