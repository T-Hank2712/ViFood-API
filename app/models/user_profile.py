from __future__ import annotations

from pydantic import BaseModel

from app.models.health_goal import HealthGoal
from app.models.disease import Disease
from app.models.allergy import Allergy


class UserProfile(BaseModel):
    profile_id: int
    userId: int | None = None
    first_name: str
    last_name: str
    avatar: str | None = None
    health_goals: list[HealthGoal] = []
    diseases: list[Disease] = []
    allergies: list[Allergy] = []
    family_members: list[UserProfile] = []
    parent_profile_id: int | None = None
