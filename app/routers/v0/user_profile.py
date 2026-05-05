from fastapi import APIRouter, HTTPException, status
from app.services.v0.user_profile_service import UserProfileServiceV0

router = APIRouter(
    prefix="/user-profile",
    tags=["User Profile v0"])


@router.get(
    "/{profile_id}",
    summary="Lấy thông tin hồ sơ người dùng",
)
async def get_user_profile(profile_id: int):
    """Lấy thông tin hồ sơ người dùng theo ID"""
    user_profile = UserProfileServiceV0.get_user_profile(profile_id)
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User profile with ID {profile_id} not found"
        )
    return user_profile


@router.get(
    "/{profile_id}/health-goals",
    summary="Lấy danh sách mục tiêu sức khỏe của hồ sơ người dùng",
)
async def get_health_goals_by_profile_id(profile_id: int):
    """Lấy danh sách mục tiêu sức khỏe của hồ sơ người dùng theo ID"""
    try:
        health_goals = UserProfileServiceV0.get_heath_goal_by_profile_id(profile_id)
        return health_goals
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/{profile_id}/diseases",
    summary="Lấy danh sách bệnh của hồ sơ người dùng",
)
async def get_diseases_by_profile_id(profile_id: int):
    """Lấy danh sách bệnh của hồ sơ người dùng theo ID"""
    try:
        diseases = UserProfileServiceV0.get_disease_by_profile_id(profile_id)
        return diseases
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/{profile_id}/allergies",
    summary="Lấy danh sách dị ứng của hồ sơ người dùng",
)
async def get_allergies_by_profile_id(profile_id: int):
    """Lấy danh sách dị ứng của hồ sơ người dùng theo ID"""
    try:
        allergies = UserProfileServiceV0.get_allergy_by_profile_id(profile_id)
        return allergies
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/{profile_id}/health-goals/{health_goal_id}",
    summary="Thêm mục tiêu sức khỏe vào hồ sơ người dùng",
)
async def add_health_goal_to_user_profile(profile_id: int, health_goal_id: int):
    """Thêm mục tiêu sức khỏe vào hồ sơ người dùng"""
    try:
        updated_profile = UserProfileServiceV0.add_health_goal(profile_id, health_goal_id)
        return updated_profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    

@router.delete(
    "/{profile_id}/health-goals/{health_goal_id}",
    summary="Xóa mục tiêu sức khỏe khỏi hồ sơ người dùng",
)
async def delete_health_goal_from_user_profile(profile_id: int, health_goal_id: int):
    """Xóa mục tiêu sức khỏe khỏi hồ sơ người dùng"""
    try:
        updated_profile = UserProfileServiceV0.delete_health_goal(profile_id, health_goal_id)
        return updated_profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    

@router.post(
    "/{profile_id}/diseases/{disease_id}",
    summary="Thêm bệnh vào hồ sơ người dùng",
)
async def add_disease_to_user_profile(profile_id: int, disease_id: int):
    """Thêm bệnh vào hồ sơ người dùng"""
    try:
        updated_profile = UserProfileServiceV0.add_disease(profile_id, disease_id)
        return updated_profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    

@router.delete(
    "/{profile_id}/diseases/{disease_id}",
    summary="Xóa bệnh khỏi hồ sơ người dùng",
)
async def delete_disease_from_user_profile(profile_id: int, disease_id: int):
    """Xóa bệnh khỏi hồ sơ người dùng"""
    try:
        updated_profile = UserProfileServiceV0.delete_disease(profile_id, disease_id)
        return updated_profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
        
        
@router.post(
    "/{profile_id}/allergies/{allergy_id}",
    summary="Thêm dị ứng vào hồ sơ người dùng",
)
async def add_allergy_to_user_profile(profile_id: int, allergy_id: int):
    """Thêm dị ứng vào hồ sơ người dùng"""
    try:
        updated_profile = UserProfileServiceV0.add_allergy(profile_id, allergy_id)
        return updated_profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
        
        
@router.delete(
    "/{profile_id}/allergies/{allergy_id}",
    summary="Xóa dị ứng khỏi hồ sơ người dùng",
)
async def delete_allergy_from_user_profile(profile_id: int, allergy_id: int):
    """Xóa dị ứng khỏi hồ sơ người dùng"""
    try:
        updated_profile = UserProfileServiceV0.delete_allergy(profile_id, allergy_id)
        return updated_profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
        

@router.post(
    "/",
    summary="Tạo hồ sơ người dùng với đầy đủ thông tin",
)
async def create_user_profile(
        profile_id: int,
        first_name: str,
        last_name: str,
        avatar: str,
        parent_profile_id: int | None = None):
    """Tạo hồ sơ người dùng với full thông tin"""
    try:
        new_profile = UserProfileServiceV0.create_user_profile(
            profile_id,
            first_name,
            last_name,
            avatar,
            parent_profile_id
        )
        return new_profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        

@router.put(
    "/{profile_id}",
    summary="Cập nhật thông tin hồ sơ người dùng",
)
async def update_user_profile(
    profile_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    avatar: str | None = None
):
    """Cập nhật thông tin hồ sơ người dùng"""
    try:
        updated_profile = UserProfileServiceV0.update_user_profile(
            profile_id,
            first_name,
            last_name,
            avatar
        )
        return updated_profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
