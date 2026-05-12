from app.models.user_profile import UserProfile

from app.models.health_goal import HealthGoal
from app.models.disease import Disease
from app.models.allergy import Allergy

from app.services.v0.health_goal_service import HealthGoalServiceV0
from app.services.v0.disease_service import DiseaseServiceV0
from app.services.v0.allergy_service import AllergyServiceV0

from app.repositories.profile_repo import UserProfileRepository

profile_repo = UserProfileRepository()


class UserProfileServiceV0:

    @staticmethod
    def get_all_user_profiles() -> list[UserProfile]:
        return profile_repo.get_all_user_profiles()

    @staticmethod
    def get_user_profile(profile_id: int) -> UserProfile:

        profile = profile_repo.get_user_profile_by_id(profile_id)

        if not profile:
            raise ValueError("UserProfile not found")

        return profile

    @staticmethod
    def create_user_profile(
        first_name: str,
        last_name: str,
        avatar: str | None = None,
        parent_profile_id: int | None = None
    ) -> UserProfile:

        # Validate
        if not first_name or not last_name:
            raise ValueError("Missing required fields")

        # Validate parent profile
        if parent_profile_id:
            parent = profile_repo.get_user_profile_by_id(
                parent_profile_id
            )

            if not parent:
                raise ValueError("Parent profile not found")

        # Create profile
        profile = UserProfile(
            profile_id=profile_repo.count_user_profiles() + 1,
            userId=None,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
            health_goals=[],
            diseases=[],
            allergies=[],
            family_members=[],
            parent_profile_id=parent_profile_id
        )

        created_profile = profile_repo.create_user_profile(profile)

        # Add family member
        if parent_profile_id:
            profile_repo.add_family_member(
                parent_profile_id,
                created_profile
            )

        return created_profile

    @staticmethod
    def update_user_profile(
        profile_id: int,
        first_name: str,
        last_name: str,
        avatar: str | None = None
    ) -> UserProfile:

        profile = profile_repo.update_user_profile(
            profile_id=profile_id,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar
        )

        if not profile:
            raise ValueError("UserProfile not found")

        return profile

    # =========================
    # HEALTH GOALS
    # =========================

    @staticmethod
    def get_health_goals(
        profile_id: int
    ) -> list[HealthGoal]:

        profile = UserProfileServiceV0.get_user_profile(profile_id)

        return profile.health_goals

    @staticmethod
    def add_health_goal(
        profile_id: int,
        health_goal_id: int
    ) -> UserProfile:
        UserProfileServiceV0.get_user_profile(profile_id)

        goal = HealthGoalServiceV0.get_health_goal_by_id(
            health_goal_id
        )

        if not goal:
            raise ValueError("HealthGoal not found")

        updated_profile = profile_repo.add_health_goal(
            profile_id,
            goal
        )

        return updated_profile

    @staticmethod
    def delete_health_goal(
        profile_id: int,
        health_goal_id: int
    ) -> UserProfile:

        profile = UserProfileServiceV0.get_user_profile(profile_id)

        updated_profile = profile_repo.delete_health_goal(
            profile.profile_id,
            health_goal_id
        )

        return updated_profile

    # =========================
    # DISEASES
    # =========================

    @staticmethod
    def get_diseases(
        profile_id: int
    ) -> list[Disease]:

        profile = UserProfileServiceV0.get_user_profile(profile_id)

        return profile.diseases

    @staticmethod
    def add_disease(
        profile_id: int,
        disease_id: int
    ) -> UserProfile:

        profile = UserProfileServiceV0.get_user_profile(profile_id)

        disease = DiseaseServiceV0.get_disease_by_id(
            disease_id
        )

        if not disease:
            raise ValueError("Disease not found")

        updated_profile = profile_repo.add_disease(
            profile.profile_id,
            disease
        )

        return updated_profile

    @staticmethod
    def delete_disease(
        profile_id: int,
        disease_id: int
    ) -> UserProfile:

        profile = UserProfileServiceV0.get_user_profile(profile_id)

        updated_profile = profile_repo.delete_disease(
            profile.profile_id,
            disease_id
        )

        return updated_profile

    # =========================
    # ALLERGIES
    # =========================

    @staticmethod
    def get_allergies(
        profile_id: int
    ) -> list[Allergy]:

        profile = UserProfileServiceV0.get_user_profile(profile_id)

        return profile.allergies

    @staticmethod
    def add_allergy(
        profile_id: int,
        allergy_id: int
    ) -> UserProfile:

        profile = UserProfileServiceV0.get_user_profile(profile_id)

        allergy = AllergyServiceV0.get_allergy_by_id(
            allergy_id
        )

        if not allergy:
            raise ValueError("Allergy not found")

        updated_profile = profile_repo.add_allergy(
            profile.profile_id,
            allergy
        )

        return updated_profile

    @staticmethod
    def delete_allergy(
        profile_id: int,
        allergy_id: int
    ) -> UserProfile:

        profile = UserProfileServiceV0.get_user_profile(profile_id)

        updated_profile = profile_repo.delete_allergy(
            profile.profile_id,
            allergy_id
        )

        return updated_profile
