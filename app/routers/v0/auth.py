from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_current_user
from app.repositories.profile_repo import UserProfileRepository
from app.repositories.user_repo import UserRepository
from app.schemas.auth import RegisterRequest
from app.services.v0.auth_service import AuthServiceV0

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

auth_service = AuthServiceV0()
profile_repo = UserProfileRepository()


@router.post("/register")
def register(data: RegisterRequest):

    user = auth_service.register_user(data)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return {
        "message": "Register success",
        "data": {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "profile_id": user.profile_id
        }
    }
    
    
@router.post("/login")
def login(email: str, password: str):
    result = auth_service.login(
        email=email,
        password=password
    )
    return {
        "message": "Login success",
        "data": result
    }
    
    
@router.post("/refresh")
def refresh_access_token(refresh_token: str):
    result = auth_service.refresh_access_token(refresh_token)

    return {
        "message": "Refresh access token success",
        "data": result
    }
