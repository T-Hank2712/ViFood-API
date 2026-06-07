from fastapi import APIRouter, Depends, HTTPException, status

from app.repositories.user_repo import UserRepository
from app.repositories.profile_repo import UserProfileRepository

from app.services.v0.user_profile_service import (
    UserProfileServiceV0
)

from app.schemas.update_profile import UpdateProfileRequest

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/user-profiles",
    tags=["User Profile v0"]
)

profile_repo = UserProfileRepository()


# =========================
# BASIC
# =========================

@router.get(
    "/",
    summary="Lấy toàn bộ hồ sơ người dùng"
)
async def get_all_user_profiles():

    profiles = UserProfileServiceV0.get_all_user_profiles()

    return {
        "message": "Get all user profiles success",
        "data": profiles
    }


@router.get(
    "/{profile_id:int}",
    summary="Lấy thông tin hồ sơ người dùng"
)
async def get_user_profile(
    profile_id: int,
    current_user=Depends(get_current_user)
):

    try:
        profile = UserProfileServiceV0.get_user_profile(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id
        )

        return {
            "message": "Get user profile success",
            "data": profile
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
        
    
@router.get(
    "/{profile_id}/family-members",
    summary="Lấy danh sách thành viên gia đình"
)
async def get_family_members(
    profile_id: int,
    current_user=Depends(get_current_user)
):

    try:
        family_members = UserProfileServiceV0.get_family_members(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id
        )

        return {
            "message": "Get family members success",
            "data": family_members
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/family-members",
    summary="Tạo hồ sơ người dùng"
)
async def create_user_profile(
    payload: UpdateProfileRequest,
    current_user=Depends(get_current_user)
):

    try:
        profile = UserProfileServiceV0.create_user_profile(
            current_user_id=current_user["user_id"],
            first_name=payload.first_name,
            last_name=payload.last_name,
            avatar=payload.avatar
        )

        return {
            "message": "Create user profile success",
            "data": profile
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.patch(
    "/{profile_id}",
    summary="Cập nhật một phần hồ sơ người dùng"
)
async def update_user_profile(
    profile_id: int,
    payload: UpdateProfileRequest,
    current_user=Depends(get_current_user)
):
    try:
        profile = UserProfileServiceV0.update_user_profile(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            payload=payload
        )

        return {
            "message": "Update user profile success",
            "data": profile
        }

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{profile_id}",
    summary="Xóa hồ sơ thành viên gia đình"
)
async def delete_user_profile(
    profile_id: int,
    current_user=Depends(get_current_user)
):

    try:
        UserProfileServiceV0.delete_user_profile(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id
        )

        return {
            "message": "Delete user profile success"
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# =========================
# HEALTH GOALS
# =========================

@router.get(
    "/{profile_id}/health-goals",
    summary="Lấy danh sách mục tiêu sức khỏe"
)
async def get_health_goals(
    profile_id: int,
    current_user=Depends(get_current_user)
):

    try:
        goals = UserProfileServiceV0.get_health_goals(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id
        )

        return {
            "message": "Get health goals success",
            "data": goals
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/{profile_id}/health-goals/{health_goal_id}",
    summary="Thêm mục tiêu sức khỏe"
)
async def add_health_goal(
    profile_id: int,
    health_goal_id: int,
    current_user=Depends(get_current_user)
):

    try:
        profile = UserProfileServiceV0.add_health_goal(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            health_goal_id=health_goal_id
        )

        return {
            "message": "Add health goal success",
            "data": profile
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{profile_id}/health-goals/{health_goal_id}",
    summary="Xóa mục tiêu sức khỏe"
)
async def delete_health_goal(
    profile_id: int,
    health_goal_id: int,
    current_user=Depends(get_current_user)
):

    try:
        profile = UserProfileServiceV0.delete_health_goal(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            health_goal_id=health_goal_id
        )

        return {
            "message": "Delete health goal success",
            "data": profile
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# =========================
# DISEASES
# =========================

@router.get(
    "/{profile_id}/diseases",
    summary="Lấy danh sách bệnh"
)
async def get_diseases(
    profile_id: int,
    current_user=Depends(get_current_user)
):

    try:
        diseases = UserProfileServiceV0.get_diseases(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id
        )

        return {
            "message": "Get diseases success",
            "data": diseases
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/{profile_id}/diseases/{disease_id}",
    summary="Thêm bệnh"
)
async def add_disease(
    profile_id: int,
    disease_id: int,
    current_user=Depends(get_current_user)
):

    try:
        profile = UserProfileServiceV0.add_disease(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            disease_id=disease_id
        )

        return {
            "message": "Add disease success",
            "data": profile
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{profile_id}/diseases/{disease_id}",
    summary="Xóa bệnh"
)
async def delete_disease(
    profile_id: int,
    disease_id: int,
    current_user=Depends(get_current_user)
):

    try:
        profile = UserProfileServiceV0.delete_disease(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            disease_id=disease_id
        )

        return {
            "message": "Delete disease success",
            "data": profile
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# =========================
# ALLERGIES
# =========================

@router.get(
    "/{profile_id}/allergies",
    summary="Lấy danh sách dị ứng"
)
async def get_allergies(
    profile_id: int,
    current_user=Depends(get_current_user)
):

    try:
        allergies = UserProfileServiceV0.get_allergies(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id
        )

        return {
            "message": "Get allergies success",
            "data": allergies
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/{profile_id}/allergies/{allergy_id}",
    summary="Thêm dị ứng"
)
async def add_allergy(
    profile_id: int,
    allergy_id: int,
    current_user=Depends(get_current_user)
):

    try:
        profile = UserProfileServiceV0.add_allergy(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            allergy_id=allergy_id
        )

        return {
            "message": "Add allergy success",
            "data": profile
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{profile_id}/allergies/{allergy_id}",
    summary="Xóa dị ứng"
)
async def delete_allergy(
    profile_id: int,
    allergy_id: int,
    current_user=Depends(get_current_user)
):

    try:
        profile = UserProfileServiceV0.delete_allergy(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            allergy_id=allergy_id
        )

        return {
            "message": "Delete allergy success",
            "data": profile
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# =========================
# CURRENT USER
# =========================

@router.get(
    "/me",
    summary="Lấy thông tin người dùng hiện tại"
)
async def me(
    current_user=Depends(get_current_user)
):

    user_id = current_user["user_id"]

    user = UserRepository.get_user_by_id(
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    profile = profile_repo.get_user_profile_by_id(
        user.profile_id
    )

    return {
        "message": "Get current user success",
        "data": {
            "user": user,
            "profile": profile
        }
    }
