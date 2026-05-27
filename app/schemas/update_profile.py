import re

from pydantic import BaseModel

class UpdateProfileRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None
