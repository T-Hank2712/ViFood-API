from fastapi import APIRouter, HTTPException, status

from app.services.v0.user_profile_service import (
    UserProfileServiceV0
)

router = APIRouter(
    prefix="/user-profiles",
    tags=["User Profile v0"]
)


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
    "/{profile_id}",
    summary="Lấy thông tin hồ sơ người dùng"
)
async def get_user_profile(profile_id: int):

    try:
        profile = UserProfileServiceV0.get_user_profile(
            profile_id
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


@router.post(
    "/",
    summary="Tạo hồ sơ người dùng"
)
async def create_user_profile(
    first_name: str,
    last_name: str,
    avatar: str | None = None,
    parent_profile_id: int | None = None
):

    try:
        profile = UserProfileServiceV0.create_user_profile(
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
            parent_profile_id=parent_profile_id
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


@router.put(
    "/{profile_id}",
    summary="Cập nhật hồ sơ người dùng"
)
async def update_user_profile(
    profile_id: int,
    first_name: str,
    last_name: str,
    avatar: str | None = None
):

    try:
        profile = UserProfileServiceV0.update_user_profile(
            profile_id=profile_id,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar
        )

        return {
            "message": "Update user profile success",
            "data": profile
        }

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
async def get_health_goals(profile_id: int):

    try:
        goals = UserProfileServiceV0.get_health_goals(
            profile_id
        )

        return {
            "message": "Get health goals success",
            "data": goals
        }

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
    health_goal_id: int
):

    try:
        profile = UserProfileServiceV0.add_health_goal(
            profile_id,
            health_goal_id
        )

        return {
            "message": "Add health goal success",
            "data": profile
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{profile_id}/health-goals/{health_goal_id}",
    summary="Xóa mục tiêu sức khỏe"
)
async def delete_health_goal(
    profile_id: int,
    health_goal_id: int
):

    try:
        profile = UserProfileServiceV0.delete_health_goal(
            profile_id,
            health_goal_id
        )

        return {
            "message": "Delete health goal success",
            "data": profile
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# =========================
# DISEASES
# =========================

@router.get(
    "/{profile_id}/diseases",
    summary="Lấy danh sách bệnh"
)
async def get_diseases(profile_id: int):

    try:
        diseases = UserProfileServiceV0.get_diseases(
            profile_id
        )

        return {
            "message": "Get diseases success",
            "data": diseases
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/{profile_id}/diseases/{disease_id}",
    summary="Thêm bệnh"
)
async def add_disease(
    profile_id: int,
    disease_id: int
):

    try:
        profile = UserProfileServiceV0.add_disease(
            profile_id,
            disease_id
        )

        return {
            "message": "Add disease success",
            "data": profile
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{profile_id}/diseases/{disease_id}",
    summary="Xóa bệnh"
)
async def delete_disease(
    profile_id: int,
    disease_id: int
):

    try:
        profile = UserProfileServiceV0.delete_disease(
            profile_id,
            disease_id
        )

        return {
            "message": "Delete disease success",
            "data": profile
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# =========================
# ALLERGIES
# =========================

@router.get(
    "/{profile_id}/allergies",
    summary="Lấy danh sách dị ứng"
)
async def get_allergies(profile_id: int):

    try:
        allergies = UserProfileServiceV0.get_allergies(
            profile_id
        )

        return {
            "message": "Get allergies success",
            "data": allergies
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/{profile_id}/allergies/{allergy_id}",
    summary="Thêm dị ứng"
)
async def add_allergy(
    profile_id: int,
    allergy_id: int
):

    try:
        profile = UserProfileServiceV0.add_allergy(
            profile_id,
            allergy_id
        )

        return {
            "message": "Add allergy success",
            "data": profile
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{profile_id}/allergies/{allergy_id}",
    summary="Xóa dị ứng"
)
async def delete_allergy(
    profile_id: int,
    allergy_id: int
):

    try:
        profile = UserProfileServiceV0.delete_allergy(
            profile_id,
            allergy_id
        )

        return {
            "message": "Delete allergy success",
            "data": profile
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
