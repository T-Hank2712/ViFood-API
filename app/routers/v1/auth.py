from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.dependencies import get_current_user
from app.helpers.convert_time import to_vn_time
from app.repositories.user_repo import UserRepository
from app.schemas.auth import (RegisterRequest, LoginRequest)
from app.services.v1.auth_service import AuthServiceV1

from app.core.database import neo4j_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth V1"]
)

auth_service = AuthServiceV1(neo4j_db)
user_repo = UserRepository(neo4j_db)


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
            "email": user.email,
            "is_active": user.is_active,
            "created_at": to_vn_time(user.created_at),
            "updated_at": to_vn_time(user.updated_at),
        }
    }
    
    
@router.post("/login")
def login(data: LoginRequest):
    result = auth_service.login(
        email=data.email,
        password=data.password
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
    

@router.get(
    "/me",
    summary="Lấy thông tin người dùng hiện tại"
)
async def me(
    current_user=Depends(get_current_user)
):

    user_id = current_user["user_id"]

    user = user_repo.get_user_by_id(
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_profile = auth_service.get_current_user(user_id)

    return {
        "message": "Get current user success",
        "data": {
            "user": user_profile.get("user"),
            "profile": user_profile.get("profile")
        }
    }
