from app.models.user_profile import UserProfile

from app.models.health_goal import HealthGoal
from app.models.disease import Disease
from app.models.allergy import Allergy

from app.services.v0.health_goal_service import HealthGoalServiceV0
from app.services.v0.disease_service import DiseaseServiceV0
from app.services.v0.allergy_service import AllergyServiceV0

from app.repositories.profile_repo import UserProfileRepository

from app.schemas.update_profile import UpdateProfileRequest

profile_repo = UserProfileRepository()


class UserProfileServiceV0:

    # =========================
    # PROFILE
    # =========================

    @staticmethod
    def get_all_user_profiles() -> list[UserProfile]:
        return profile_repo.get_all_user_profiles()

    @staticmethod
    def get_user_profile(
        current_user_id: int,
        target_profile_id: int
    ) -> UserProfile:

        profile = profile_repo.get_user_profile_by_id(
            target_profile_id
        )

        if not profile:
            raise ValueError("UserProfile not found")

        # 1. owner access
        if profile.userId == current_user_id:
            return profile

        # 2. parent access
        if profile.parent_profile_id:
            parent = profile_repo.get_user_profile_by_id(
                profile.parent_profile_id
            )

            if parent and parent.userId == current_user_id:
                return profile

        # 3. family access
        if any(
            member.userId == current_user_id
            for member in profile.family_members
        ):
            return profile

        raise PermissionError(
            "You cannot access this profile"
        )

    @staticmethod
    def create_user_profile(
        current_user_id: int,
        first_name: str,
        last_name: str,
        avatar: str | None = None
    ) -> UserProfile:

        if not first_name.strip():
            raise ValueError("First name is required")

        if not last_name.strip():
            raise ValueError("Last name is required")

        # tìm profile chính của user hiện tại
        parent_profile = profile_repo.get_user_profile_by_user_id(
            current_user_id
        )

        if not parent_profile:
            raise ValueError("Parent profile not found")

        profile = UserProfile(
            profile_id=profile_repo.count_user_profiles() + 1,
            userId=None,
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            avatar=avatar,
            health_goals=[],
            diseases=[],
            allergies=[],
            family_members=[],
            parent_profile_id=parent_profile.profile_id
        )

        created_profile = profile_repo.create_user_profile(
            profile
        )

        profile_repo.add_family_member(
            parent_profile.profile_id,
            created_profile
        )

        return created_profile

    @staticmethod
    def update_user_profile(
        current_user_id: int,
        target_profile_id: int,
        payload: UpdateProfileRequest
    ) -> UserProfile:

        UserProfileServiceV0._validate_profile_access(
            current_user_id,
            target_profile_id
        )

        profile = profile_repo.get_user_profile_by_id(target_profile_id)

        if not profile:
            raise ValueError("UserProfile not found")

        updated_first_name = (
            payload.first_name.strip()
            if payload.first_name is not None
            else profile.first_name
        )

        updated_last_name = (
            payload.last_name.strip()
            if payload.last_name is not None
            else profile.last_name
        )

        updated_avatar = (
            payload.avatar
            if payload.avatar is not None
            else profile.avatar
        )

        if payload.first_name is not None and not updated_first_name:
            raise ValueError("First name cannot be empty")

        if payload.last_name is not None and not updated_last_name:
            raise ValueError("Last name cannot be empty")

        return profile_repo.update_user_profile(
            profile_id=target_profile_id,
            first_name=updated_first_name,
            last_name=updated_last_name,
            avatar=updated_avatar
        )

    # =========================
    # HEALTH GOALS
    # =========================

    @staticmethod
    def get_health_goals(
        current_user_id: int,
        target_profile_id: int
    ) -> list[HealthGoal]:

        profile = UserProfileServiceV0.get_user_profile(
            current_user_id,
            target_profile_id
        )

        return profile.health_goals

    @staticmethod
    def add_health_goal(
        current_user_id: int,
        target_profile_id: int,
        health_goal_id: int
    ) -> UserProfile:

        UserProfileServiceV0._validate_profile_access(
            current_user_id,
            target_profile_id
        )

        goal = HealthGoalServiceV0.get_health_goal_by_id(
            health_goal_id
        )

        if not goal:
            raise ValueError("Health goal not found")

        return profile_repo.add_health_goal(
            target_profile_id,
            goal
        )

    @staticmethod
    def delete_health_goal(
        current_user_id: int,
        target_profile_id: int,
        health_goal_id: int
    ) -> UserProfile:

        UserProfileServiceV0._validate_profile_access(
            current_user_id,
            target_profile_id
        )

        goal = HealthGoalServiceV0.get_health_goal_by_id(
            health_goal_id
        )

        if not goal:
            raise ValueError("Health goal not found")

        return profile_repo.delete_health_goal(
            target_profile_id,
            health_goal_id
        )

    # =========================
    # DISEASES
    # =========================

    @staticmethod
    def get_diseases(
        current_user_id: int,
        target_profile_id: int
    ) -> list[Disease]:

        profile = UserProfileServiceV0.get_user_profile(
            current_user_id,
            target_profile_id
        )

        return profile.diseases

    @staticmethod
    def add_disease(
        current_user_id: int,
        target_profile_id: int,
        disease_id: int
    ) -> UserProfile:

        UserProfileServiceV0._validate_profile_access(
            current_user_id,
            target_profile_id
        )

        disease = DiseaseServiceV0.get_disease_by_id(
            disease_id
        )

        if not disease:
            raise ValueError("Disease not found")

        return profile_repo.add_disease(
            target_profile_id,
            disease
        )

    @staticmethod
    def delete_disease(
        current_user_id: int,
        target_profile_id: int,
        disease_id: int
    ) -> UserProfile:

        UserProfileServiceV0._validate_profile_access(
            current_user_id,
            target_profile_id
        )

        disease = DiseaseServiceV0.get_disease_by_id(
            disease_id
        )

        if not disease:
            raise ValueError("Disease not found")

        return profile_repo.delete_disease(
            target_profile_id,
            disease_id
        )

    # =========================
    # ALLERGIES
    # =========================

    @staticmethod
    def get_allergies(
        current_user_id: int,
        target_profile_id: int
    ) -> list[Allergy]:

        profile = UserProfileServiceV0.get_user_profile(
            current_user_id,
            target_profile_id
        )

        return profile.allergies

    @staticmethod
    def add_allergy(
        current_user_id: int,
        target_profile_id: int,
        allergy_id: int
    ) -> UserProfile:

        UserProfileServiceV0._validate_profile_access(
            current_user_id,
            target_profile_id
        )

        allergy = AllergyServiceV0.get_allergy_by_id(
            allergy_id
        )

        if not allergy:
            raise ValueError("Allergy not found")

        return profile_repo.add_allergy(
            target_profile_id,
            allergy
        )

    @staticmethod
    def delete_allergy(
        current_user_id: int,
        target_profile_id: int,
        allergy_id: int
    ) -> UserProfile:

        UserProfileServiceV0._validate_profile_access(
            current_user_id,
            target_profile_id
        )

        allergy = AllergyServiceV0.get_allergy_by_id(
            allergy_id
        )

        if not allergy:
            raise ValueError("Allergy not found")

        return profile_repo.delete_allergy(
            target_profile_id,
            allergy_id
        )

    # =========================
    # ACCESS CONTROL
    # =========================

    @staticmethod
    def can_access_profile(
        current_user_id: int,
        target_profile_id: int
    ) -> bool:

        profile = profile_repo.get_user_profile_by_id(
            target_profile_id
        )

        if not profile:
            return False

        # owner
        if profile.userId == current_user_id:
            return True

        # parent
        if profile.parent_profile_id:
            parent = profile_repo.get_user_profile_by_id(
                profile.parent_profile_id
            )

            if parent and parent.userId == current_user_id:
                return True

        # family
        if any(
            member.userId == current_user_id
            for member in profile.family_members
        ):
            return True

        return False

    @staticmethod
    def _validate_profile_access(
        current_user_id: int,
        target_profile_id: int
    ) -> None:

        if not UserProfileServiceV0.can_access_profile(
            current_user_id,
            target_profile_id
        ):
            raise PermissionError("Access denied")
