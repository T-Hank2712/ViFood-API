from app.models.user_profile import UserProfile

from app.models.health_goal import HealthGoal
from app.models.disease import Disease
from app.models.allergy import Allergy

from app.services.v0.health_goal_service import HealthGoalServiceV0
from app.services.v0.disease_service import DiseaseServiceV0
from app.services.v0.allergy_service import AllergyServiceV0

user_profile = [
    UserProfile(
        profile_id=1,
        userId=1,
        firstName="Thành",
        lastName="Lâm",
        avatar="https://example.com/avatar.jpg",
        health_goals=[
            HealthGoal(id=1, name="Giảm cân"),
        ],
        diseases=[
            Disease(id=1, name="Tiểu đường"),
        ],
        allergies=[
            Allergy(id=1, name="Gluten"),
        ],
        family_members=[],
    ),
]


class UserProfileServiceV0:
    @staticmethod
    def get_user_profile(profile_id: int) -> UserProfile | None:
        return next((n for n in user_profile if n.profile_id == profile_id), None)
    
    @staticmethod
    def get_health_goal_by_profile_id(profile_id: int) -> list[HealthGoal]:
        profile = UserProfileServiceV0.get_user_profile(profile_id)
        if not profile:
            raise ValueError("UserProfile not found")
        return profile.health_goals

    @staticmethod
    def add_health_goal(profile_id: int, health_goal_id: int) -> UserProfile:
        profile = UserProfileServiceV0.get_user_profile(profile_id)
        if not profile:
            raise ValueError("UserProfile not found")

        goal = HealthGoalServiceV0.get_health_goal_by_id(health_goal_id)
        if not goal:
            raise ValueError("HealthGoal not found")

        if any(g.id == health_goal_id for g in profile.health_goals):
            return profile

        profile.health_goals.append(goal)

        return profile
    
    @staticmethod
    def delete_health_goal(profile_id: int, health_goal_id: int) -> UserProfile:
        profile = UserProfileServiceV0.get_user_profile(profile_id)
        if not profile:
            raise ValueError("UserProfile not found")

        goal = HealthGoalServiceV0.get_health_goal_by_id(health_goal_id)
        if not goal:
            raise ValueError("HealthGoal not found")

        profile.health_goals = [g for g in profile.health_goals if g.id != health_goal_id]

        return profile
    
    @staticmethod
    def get_disease_by_profile_id(profile_id: int) -> list[Disease]:
        profile = UserProfileServiceV0.get_user_profile(profile_id)
        if not profile:
            raise ValueError("UserProfile not found")
        return profile.diseases
    
    @staticmethod
    def add_disease(profile_id: int, disease_id: int) -> UserProfile:
        profile = UserProfileServiceV0.get_user_profile(profile_id)
        if not profile:
            raise ValueError("UserProfile not found")

        disease = DiseaseServiceV0.get_disease_by_id(disease_id)
        if not disease:
            raise ValueError("Disease not found")

        if any(d.id == disease_id for d in profile.diseases):
            return profile

        profile.diseases.append(disease)

        return profile
    
    @staticmethod
    def delete_disease(profile_id: int, disease_id: int) -> UserProfile:
        profile = UserProfileServiceV0.get_user_profile(profile_id)
        if not profile:
            raise ValueError("UserProfile not found")

        disease = DiseaseServiceV0.get_disease_by_id(disease_id)
        if not disease:
            raise ValueError("Disease not found")

        profile.diseases = [d for d in profile.diseases if d.id != disease_id]

        return profile
    
    @staticmethod
    def get_allergy_by_profile_id(profile_id: int) -> list[Allergy]:
        profile = UserProfileServiceV0.get_user_profile(profile_id)
        if not profile:
            raise ValueError("UserProfile not found")
        return profile.allergies
    
    @staticmethod
    def add_allergy(profile_id: int, allergy_id: int) -> UserProfile:
        profile = UserProfileServiceV0.get_user_profile(profile_id)
        if not profile:
            raise ValueError("UserProfile not found")

        allergy = AllergyServiceV0.get_allergy_by_id(allergy_id)
        if not allergy:
            raise ValueError("Allergy not found")

        if any(a.id == allergy_id for a in profile.allergies):
            return profile

        profile.allergies.append(allergy)

        return profile
    
    @staticmethod
    def delete_allergy(profile_id: int, allergy_id: int) -> UserProfile:
        profile = UserProfileServiceV0.get_user_profile(profile_id)
        if not profile:
            raise ValueError("UserProfile not found")

        allergy = AllergyServiceV0.get_allergy_by_id(allergy_id)
        if not allergy:
            raise ValueError("Allergy not found")

        profile.allergies = [a for a in profile.allergies if a.id != allergy_id]

        return profile

    @staticmethod
    def create_user_profile(
        profile_id: int,
        first_name: str,
        last_name: str,
        avatar: str,
        parent_profile_id: int | None = None
    ) -> UserProfile:

        # 1. Validate
        if not first_name or not last_name:
            raise ValueError("Missing required fields")

        # 2. Tạo profile
        new_profile = UserProfile(
            profile_id=profile_id,
            parent_profile_id=parent_profile_id,
            firstName=first_name,
            lastName=last_name,
            avatar=avatar,
            health_goals=[],
            diseases=[],
            allergies=[],
            family_members=[]
        )

        # 3. Nếu có parent → add vào family_members
        if parent_profile_id:
            parent = UserProfileServiceV0.get_user_profile(parent_profile_id)
            if not parent:
                raise ValueError("Parent profile not found")

            parent.family_members.append(new_profile)

        # 5. Lưu vào list chính
        user_profile.append(new_profile)

        return new_profile

    @staticmethod
    def update_user_profile(
        profile_id: int,
        first_name: str,
        last_name: str,
        avatar: str | None = None
    ) -> UserProfile:
        profile = UserProfileServiceV0.get_user_profile(profile_id)
        if not profile:
            raise ValueError("UserProfile not found")

        profile.firstName = first_name
        profile.lastName = last_name
        if avatar is not None:
            profile.avatar = avatar

        return profile
