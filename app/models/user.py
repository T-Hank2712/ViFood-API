from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    password_hash: str
    is_active: bool = True
    created_at: str
    updated_at: str
    profile_id: int
