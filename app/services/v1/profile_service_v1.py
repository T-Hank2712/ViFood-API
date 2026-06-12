
from app.models.user_profile import UserProfile

# from app.services.v0.health_goal_service import HealthGoalServiceV0
from app.services.v1.disease_service_v1 import DiseaseServiceV1
from app.services.v0.allergy_service import AllergyServiceV0

from app.repositories.profile_repo import UserProfileRepository
from app.repositories.user_repo import UserRepository
from app.schemas.update_profile import UpdateProfileRequest

from app.core.database import neo4j_db

# health_goal_service = HealthGoalServiceV0()
disease_service = DiseaseServiceV1(neo4j_db)
# health_goal_service = HealthGoalServiceV0()
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
    
    def get_accessible_profile(self, current_user_id: str, profile_id: str) -> UserProfile:
        
        profile = self.profile_repo.get_profile_by_user_access(
            current_user_id,
            profile_id
        )
        
        if not profile:
            raise ValueError("Profile not found")

        return profile
    
    def update_user_profile(self, current_user_id: str, profile_id: str, profile: UpdateProfileRequest) -> UserProfile:
        
        first_name = profile.first_name.strip()
        last_name = profile.last_name.strip()

        if not first_name:
            raise ValueError("First name is required")

        if not last_name:
            raise ValueError("Last name is required")
        
        profile = self.profile_repo.update_user_profile(
            current_user_id,
            profile_id,
            profile
        )
        
        if not profile:
            raise ValueError("Profile not found")
        
        return profile
    
    def delete_family_meber(self, current_user_id: str, target_profile_id: str) -> bool:
        
        deleted = self.profile_repo.delete_family_member(
            current_user_id,
            target_profile_id
        )
        if not deleted:
            raise ValueError("Profile not found")

        return True
        
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
