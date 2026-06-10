from __future__ import annotations
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    profile_id: Optional[str] = None
    first_name: str
    last_name: str
    avatar: str | None = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
