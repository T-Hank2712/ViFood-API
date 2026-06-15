from pydantic import BaseModel


class searchDTO(BaseModel):
    id: str
    name: str
    key: str
    code: str | None = None
    description: str | None = None
    type: str
