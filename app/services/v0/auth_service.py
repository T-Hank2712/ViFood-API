from datetime import datetime
from fastapi import HTTPException, status

from app.models.user import User
from app.models.user_profile import UserProfile
from app.repositories.user_repo import UserRepository
from app.repositories.profile_repo import UserProfileRepository
from app.core.security import (hash_password, create_access_token, verify_password, verify_token, create_refresh_token)


class AuthServiceV0:

    def __init__(self):
        self.user_repo = UserRepository()
        self.profile_repo = UserProfileRepository()

    def register_user(self, data):
        existing_user = self.user_repo.get_user_by_email(data.email)

        if existing_user:
            raise ValueError("Email already exists")

        profile = UserProfile(
            profile_id=self.profile_repo.count_user_profiles() + 1,
            userId=None,
            first_name=data.first_name,
            last_name=data.last_name,
            avatar=None,
            health_goals=[],
            diseases=[],
            allergies=[],
            family_members=[],
            parent_profile_id=None
        )

        user = User(
            id=self.user_repo.count_users() + 1,
            email=data.email,
            password_hash=hash_password(data.password),
            is_active=True,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat(),
            profile_id=profile.profile_id
        )

        created_profile = self.profile_repo.create_user_profile(profile)

        created_user = self.user_repo.create_user(user)

        created_profile.userId = created_user.id

        return created_user

    def login(self, email: str, password: str) -> User | None:
        user = self.user_repo.get_user_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email hoặc mật khẩu không đúng"
            )
            
        is_valid_password = verify_password(password, user.password_hash)

        if not is_valid_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email hoặc mật khẩu không đúng"
            )

        payload = {
            "user_id": user.id,
            "email": user.email,
            "profile_id": user.profile_id,
        }

        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_access_token(self, refresh_token: str):
        payload = verify_token(refresh_token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        new_payload = {
            "user_id": payload["user_id"],
            "email": payload["email"]
        }

        new_access_token = create_access_token(new_payload)

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
