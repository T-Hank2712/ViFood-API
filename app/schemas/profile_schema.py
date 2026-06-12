from pydantic import BaseModel
    

class HealthProfileRequest(BaseModel):
    name: str
