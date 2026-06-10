# from fastapi import APIRouter, HTTPException

# from app.repositories.profile_repo import UserProfileRepository
# from app.schemas.auth import (RegisterRequest, LoginRequest)
# from app.services.v0.auth_service import AuthServiceV0

# from app.db import db

# router = APIRouter(
#     prefix="/auth",
#     tags=["Auth"]
# )

# auth_service = AuthServiceV0()
# profile_repo = UserProfileRepository(db)


# @router.post("/register")
# def register(data: RegisterRequest):

#     user = auth_service.register_user(data)

#     if not user:
#         raise HTTPException(
#             status_code=400,
#             detail="Email already exists"
#         )

#     return {
#         "message": "Register success",
#         "data": {
#             "id": user.id,
#             "email": user.email,
#             "is_active": user.is_active,
#             "created_at": user.created_at,
#             "updated_at": user.updated_at
#         }
#     }
    
    
# @router.post("/login")
# def login(data: LoginRequest):
#     result = auth_service.login(
#         email=data.email,
#         password=data.password
#     )
#     return {
#         "message": "Login success",
#         "data": result
#     }
    
    
# @router.post("/refresh")
# def refresh_access_token(refresh_token: str):
#     result = auth_service.refresh_access_token(refresh_token)

#     return {
#         "message": "Refresh access token success",
#         "data": result
#     }
