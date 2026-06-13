from fastapi import APIRouter, Depends, HTTPException, status

from app.repositories.profile_repo import UserProfileRepository

from app.services.v1.profile_service_v1 import (
    UserProfileServiceV1
)

from app.schemas.update_profile import UpdateProfileRequest

from app.core.database import neo4j_db

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/user-profiles",
    tags=["User Profile v1"]
)

profile_service = UserProfileServiceV1(neo4j_db)
profile_repo = UserProfileRepository(neo4j_db)


# =========================
# BASIC
# =========================

    
@router.get(
    "/family-members",
    summary="Lấy danh sách thành viên gia đình"
)
async def get_family_members(
    current_user=Depends(get_current_user)
):

    try:
        family_members = profile_service.get_family_members(
            current_user_id=current_user["user_id"]
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


@router.get(
    "/family-members/{profile_id}",
    summary="Lấy chi tiết thành viên gia đình"
)
async def get_family_member_detail(
    profile_id: str,
    current_user=Depends(get_current_user)
):

    try:
        profile = profile_service.get_accessible_profile(
            current_user_id=current_user["user_id"],
            profile_id=profile_id
        )

        return {
            "message": "Get profile success",
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


@router.post(
    "/family-members",
    summary="Tạo hồ sơ thành viên gia đình"
)
async def create_user_profile(
    payload: UpdateProfileRequest,
    current_user=Depends(get_current_user)
):

    try:
        profile = profile_service.create_user_profile(
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
    summary="Chỉnh sửa hồ sơ người dùng"
)
async def update_current_user_profile(
    payload: UpdateProfileRequest,
    profile_id: str,
    current_user=Depends(get_current_user),
):
    try:
        profile = profile_service.update_user_profile(
            current_user_id=current_user["user_id"],
            profile_id=profile_id,
            profile=payload
        )

        return {
            "message": "Update user profile success",
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


@router.delete(
    "/{profile_id}",
    summary="Xóa hồ sơ thành viên gia đình"
)
async def delete_user_profile(
    profile_id: str,
    current_user=Depends(get_current_user)
):

    try:
        success = profile_service.delete_family_member(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
        )

        return {
            "message": "Delete user profile success",
            "data": success
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


# # =========================
# # HEALTH GOALS
# # =========================

@router.get(
    "/{profile_id}/health-goals",
    summary="Lấy danh sách mục tiêu sức khỏe"
)
async def get_health_goals(
    profile_id: str,
    current_user=Depends(get_current_user)
):

    try:
        goals = profile_service.get_health_goals_by_profile_id(
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
    profile_id: str,
    health_goal_id: str,
    current_user=Depends(get_current_user)
):

    try:
        profile = profile_service.add_health_goal_to_profile(
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{profile_id}/health-goals/{health_goal_id}",
    summary="Xóa mục tiêu sức khỏe trong hồ sơ"
)
async def remove_health_goal(
    profile_id: str,
    health_goal_id: str,
    current_user=Depends(get_current_user)
):

    try:
        success = profile_service.remove_health_goal_from_profile(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            health_goal_id=health_goal_id
        )

        return {
            "message": "Delete health goal success",
            "data": success
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


# # =========================
# # DISEASES
# # =========================

@router.get(
    "/{profile_id}/diseases",
    summary="Lấy danh sách bệnh nền"
)
async def get_diseases(
    profile_id: str,
    current_user=Depends(get_current_user)
):

    try:
        diseases = profile_service.get_diseases_by_profile_id(
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/{profile_id}/diseases/{disease_id}",
    summary="Thêm bệnh nền"
)
async def add_disease(
    profile_id: str,
    disease_id: str,
    current_user=Depends(get_current_user)
):

    try:
        success = profile_service.add_disease_to_profile(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            disease_id=disease_id
        )

        return {
            "message": "Add disease success",
            "data": success
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
    "/{profile_id}/diseases/{disease_id}",
    summary="Xóa bệnh nền khỏi hồ sơ"
)
async def remove_disease(
    profile_id: str,
    disease_id: str,
    current_user=Depends(get_current_user)
):

    try:
        success = profile_service.remove_disease_from_profile(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            disease_id=disease_id
        )

        return {
            "message": "Delete disease success",
            "data": success
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


# # =========================
# # ALLERGIES
# # =========================

@router.get(
    "/{profile_id}/allergies",
    summary="Lấy danh sách dị ứng"
)
async def get_allergies(
    profile_id: str,
    current_user=Depends(get_current_user)
):

    try:
        allergies = profile_service.get_allergies_by_profile_id(
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/{profile_id}/allergies/{allergy_id}",
    summary="Thêm dị ứng vào hồ sơ"
)
async def add_allergy(
    profile_id: str,
    allergy_id: str,
    current_user=Depends(get_current_user)
):

    try:
        success = profile_service.add_allergy_to_profile(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            allergy_id=allergy_id
        )

        return {
            "message": "Add allergy success",
            "data": success
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
    "/{profile_id}/allergies/{allergy_id}",
    summary="Xóa dị ứng khỏi hồ sơ"
)
async def remove_allergy(
    profile_id: str,
    allergy_id: str,
    current_user=Depends(get_current_user)
):

    try:
        success = profile_service.remove_allergy_from_profile(
            current_user_id=current_user["user_id"],
            target_profile_id=profile_id,
            allergy_id=allergy_id
        )

        return {
            "message": "Delete allergy success",
            "data": success
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
