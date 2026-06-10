
from app.models.user_profile import UserProfile

from app.services.v0.health_goal_service import HealthGoalServiceV0
from app.services.v0.disease_service import DiseaseServiceV0
from app.services.v0.allergy_service import AllergyServiceV0

from app.repositories.profile_repo import UserProfileRepository
from app.repositories.user_repo import UserRepository

health_goal_service = HealthGoalServiceV0()
disease_service = DiseaseServiceV0()
allergy_service = AllergyServiceV0()


class UserProfileServiceV1:
    
    def __init__(self, db):
        self.user_repo = UserRepository(db)
        self.profile_repo = UserProfileRepository(db)
    
    # def __init__(self):
    #     self.profile_repo = UserProfileRepository(db)

    # =========================
    # PROFILE
    # =========================
        
    def get_family_members(
        self,
        current_user_id: int,
    ) -> list[UserProfile]:

        profile = self.profile_repo.get_family_members(
            current_user_id
        )

        return profile

    def create_user_profile(
        self,
        current_user_id: str,
        first_name: str,
        last_name: str,
        avatar: str | None = None
    ) -> UserProfile:

        first_name = first_name.strip()
        last_name = last_name.strip()

        if not first_name:
            raise ValueError("First name is required")

        if not last_name:
            raise ValueError("Last name is required")

        existing_profile = self.profile_repo.get_user_profile_by_user_id(current_user_id)

        if existing_profile:
            raise ValueError("User already has a profile")

        profile = UserProfile(
            first_name=first_name,
            last_name=last_name,
            avatar=avatar
        )

        created_profile = self.profile_repo.create_profile(
            user_id=current_user_id,
            profile=profile
        )

        return created_profile
    
    def get_profile_by_profile_id(self, current_user_id: str, profile_id: str) -> UserProfile:
        
        profile = self.profile_repo.get_profile_by_profile_id(
            current_user_id,
            profile_id
        )
        
        if not profile:
            raise ValueError("Profile not found")

        return profile

    # def update_user_profile(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int,
    #     payload: UpdateProfileRequest
    # ) -> UserProfile:

    #     self._validate_profile_access(
    #         current_user_id,
    #         target_profile_id
    #     )

    #     profile = self.profile_repo.get_user_profile_by_id(target_profile_id)

    #     if not profile:
    #         raise ValueError("UserProfile not found")

    #     updated_first_name = (
    #         payload.first_name.strip()
    #         if payload.first_name is not None
    #         else profile.first_name
    #     )

    #     updated_last_name = (
    #         payload.last_name.strip()
    #         if payload.last_name is not None
    #         else profile.last_name
    #     )

    #     updated_avatar = (
    #         payload.avatar
    #         if payload.avatar is not None
    #         else profile.avatar
    #     )

    #     if payload.first_name is not None and not updated_first_name:
    #         raise ValueError("First name cannot be empty")

    #     if payload.last_name is not None and not updated_last_name:
    #         raise ValueError("Last name cannot be empty")

    #     return self.profile_repo.update_user_profile(
    #         profile_id=target_profile_id,
    #         first_name=updated_first_name,
    #         last_name=updated_last_name,
    #         avatar=updated_avatar
    #     )
        
    # def delete_user_profile(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int
    # ) -> bool:

    #     profile = self.profile_repo.get_user_profile_by_id(
    #         target_profile_id
    #     )

    #     if not profile:
    #         raise ValueError("UserProfile not found")

    #     # Chỉ được xóa family member của mình
    #     if profile.parent_profile_id is None:
    #         raise PermissionError(
    #             "You can only delete family members"
    #         )

    #     parent = self.profile_repo.get_user_profile_by_id(
    #         profile.parent_profile_id
    #     )

    #     if not parent:
    #         raise ValueError("Parent profile not found")

    #     if parent.userId != current_user_id:
    #         raise PermissionError(
    #             "You can only delete your own family members"
    #         )

    #     return self.profile_repo.delete_user_profile(
    #         target_profile_id
    #     )
        
    # # =========================
    # # HEALTH GOALS
    # # =========================

    # def get_health_goals(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int
    # ) -> list[HealthGoal]:

    #     profile = self.get_user_profile(
    #         current_user_id,
    #         target_profile_id
    #     )

    #     return profile.health_goals

    # def add_health_goal(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int,
    #     health_goal_id: int
    # ) -> UserProfile:

    #     self._validate_profile_access(
    #         current_user_id,
    #         target_profile_id
    #     )

    #     goal = health_goal_service.get_health_goal_by_id(
    #         health_goal_id
    #     )

    #     if not goal:
    #         raise ValueError("Health goal not found")

    #     return self.profile_repo.add_health_goal(
    #         target_profile_id,
    #         goal
    #     )

    # def delete_health_goal(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int,
    #     health_goal_id: int
    # ) -> UserProfile:

    #     self._validate_profile_access(
    #         current_user_id,
    #         target_profile_id
    #     )

    #     goal = health_goal_service.get_health_goal_by_id(
    #         health_goal_id
    #     )

    #     if not goal:
    #         raise ValueError("Health goal not found")

    #     return self.profile_repo.delete_health_goal(
    #         target_profile_id,
    #         health_goal_id
    #     )

    # # =========================
    # # DISEASES
    # # =========================

    # def get_diseases(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int
    # ) -> list[Disease]:

    #     profile = self.get_user_profile(
    #         current_user_id,
    #         target_profile_id
    #     )

    #     return profile.diseases

    # def add_disease(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int,
    #     disease_id: int
    # ) -> UserProfile:

    #     self._validate_profile_access(
    #         current_user_id,
    #         target_profile_id
    #     )

    #     disease = disease_service.get_disease_by_id(
    #         disease_id
    #     )

    #     if not disease:
    #         raise ValueError("Disease not found")

    #     return self.profile_repo.add_disease(
    #         target_profile_id,
    #         disease
    #     )

    # def delete_disease(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int,
    #     disease_id: int
    # ) -> UserProfile:

    #     self._validate_profile_access(
    #         current_user_id,
    #         target_profile_id
    #     )

    #     disease = disease_service.get_disease_by_id(
    #         disease_id
    #     )

    #     if not disease:
    #         raise ValueError("Disease not found")

    #     return self.profile_repo.delete_disease(
    #         target_profile_id,
    #         disease_id
    #     )

    # # =========================
    # # ALLERGIES
    # # =========================

    # def get_allergies(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int
    # ) -> list[Allergy]:

    #     profile = self.get_user_profile(
    #         current_user_id,
    #         target_profile_id
    #     )

    #     return profile.allergies

    # def add_allergy(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int,
    #     allergy_id: int
    # ) -> UserProfile:

    #     self._validate_profile_access(
    #         current_user_id,
    #         target_profile_id
    #     )

    #     allergy = allergy_service.get_allergy_by_id(
    #         allergy_id
    #     )

    #     if not allergy:
    #         raise ValueError("Allergy not found")

    #     return self.profile_repo.add_allergy(
    #         target_profile_id,
    #         allergy
    #     )

    # def delete_allergy(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int,
    #     allergy_id: int
    # ) -> UserProfile:

    #     self._validate_profile_access(
    #         current_user_id,
    #         target_profile_id
    #     )

    #     allergy = allergy_service.get_allergy_by_id(
    #         allergy_id
    #     )

    #     if not allergy:
    #         raise ValueError("Allergy not found")

    #     return self.profile_repo.delete_allergy(
    #         target_profile_id,
    #         allergy_id
    #     )

    # # =========================
    # # ACCESS CONTROL
    # # =========================

    # def can_access_profile(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int
    # ) -> bool:

    #     profile = self.profile_repo.get_user_profile_by_id(
    #         target_profile_id
    #     )

    #     if not profile:
    #         return False

    #     # owner
    #     if profile.userId == current_user_id:
    #         return True

    #     # parent
    #     if profile.parent_profile_id:
    #         parent = self.profile_repo.get_user_profile_by_id(
    #             profile.parent_profile_id
    #         )

    #         if parent and parent.userId == current_user_id:
    #             return True

    #     # family
    #     if any(
    #         member.userId == current_user_id
    #         for member in profile.family_members
    #     ):
    #         return True

    #     return False

    # def _validate_profile_access(
    #     self,
    #     current_user_id: int,
    #     target_profile_id: int
    # ) -> None:

    #     if not self.can_access_profile(
    #         current_user_id,
    #         target_profile_id
    #     ):
    #         raise PermissionError("Access denied")
