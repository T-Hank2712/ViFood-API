from app.models.user_profile import UserProfile
from app.models.health_goal import HealthGoal
from app.models.disease import Disease
from app.models.allergy import Allergy


# =========================
# FAKE DATABASE
# =========================

fake_user_profiles_db: list[UserProfile] = [
    UserProfile(
        profile_id=1,
        user_id=1,
        first_name="Thành",
        last_name="Lâm",
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
        parent_profile_id=None
    ),
]


class UserProfileRepository:

    # =========================
    # BASIC
    # =========================

    def get_all_user_profiles(self) -> list[UserProfile]:
        return fake_user_profiles_db

    def count_user_profiles(self) -> int:
        return len(fake_user_profiles_db)

    def get_user_profile_by_id(
        self,
        profile_id: int
    ) -> UserProfile | None:

        return next(
            (
                profile
                for profile in fake_user_profiles_db
                if profile.profile_id == profile_id
            ),
            None
        )

    def create_user_profile(
        self,
        profile: UserProfile
    ) -> UserProfile:

        fake_user_profiles_db.append(profile)

        return profile

    def update_user_profile(
        self,
        profile_id: int,
        first_name: str,
        last_name: str,
        avatar: str | None = None
    ) -> UserProfile | None:

        profile = self.get_user_profile_by_id(profile_id)

        if profile is None:
            return None

        profile.first_name = first_name
        profile.last_name = last_name

        if avatar is not None:
            profile.avatar = avatar

        return profile

    def delete_user_profile(
        self,
        profile_id: int
    ) -> bool:

        profile = self.get_user_profile_by_id(profile_id)

        if profile is None:
            return False

        fake_user_profiles_db.remove(profile)

        return True

    # =========================
    # HEALTH GOALS
    # =========================

    def get_health_goals_by_profile_id(
        self,
        profile_id: int
    ) -> list[HealthGoal]:

        profile = self.get_user_profile_by_id(profile_id)

        if profile is None:
            return []

        return profile.health_goals

    def add_health_goal(
        self,
        profile_id: int,
        health_goal: HealthGoal
    ) -> UserProfile | None:

        profile = self.get_user_profile_by_id(profile_id)

        if profile is None:
            return None

        exists = any(
            goal.id == health_goal.id
            for goal in profile.health_goals
        )

        if exists:
            return profile

        profile.health_goals.append(health_goal)

        return profile

    def delete_health_goal(
        self,
        profile_id: int,
        health_goal_id: int
    ) -> UserProfile | None:

        profile = self.get_user_profile_by_id(profile_id)

        if profile is None:
            return None

        profile.health_goals = [
            goal
            for goal in profile.health_goals
            if goal.id != health_goal_id
        ]

        return profile

    # =========================
    # DISEASES
    # =========================

    def get_diseases_by_profile_id(
        self,
        profile_id: int
    ) -> list[Disease]:

        profile = self.get_user_profile_by_id(profile_id)

        if profile is None:
            return []

        return profile.diseases

    def add_disease(
        self,
        profile_id: int,
        disease: Disease
    ) -> UserProfile | None:

        profile = self.get_user_profile_by_id(profile_id)

        if profile is None:
            return None

        exists = any(
            d.id == disease.id
            for d in profile.diseases
        )

        if exists:
            return profile

        profile.diseases.append(disease)

        return profile

    def delete_disease(
        self,
        profile_id: int,
        disease_id: int
    ) -> UserProfile | None:

        profile = self.get_user_profile_by_id(profile_id)

        if profile is None:
            return None

        profile.diseases = [
            disease
            for disease in profile.diseases
            if disease.id != disease_id
        ]

        return profile

    # =========================
    # ALLERGIES
    # =========================

    def get_allergies_by_profile_id(
        self,
        profile_id: int
    ) -> list[Allergy]:

        profile = self.get_user_profile_by_id(profile_id)

        if profile is None:
            return []

        return profile.allergies

    def add_allergy(
        self,
        profile_id: int,
        allergy: Allergy
    ) -> UserProfile | None:

        profile = self.get_user_profile_by_id(profile_id)

        if profile is None:
            return None

        exists = any(
            allergy_item.id == allergy.id
            for allergy_item in profile.allergies
        )

        if exists:
            return profile

        profile.allergies.append(allergy)

        return profile

    def delete_allergy(
        self,
        profile_id: int,
        allergy_id: int
    ) -> UserProfile | None:

        profile = self.get_user_profile_by_id(profile_id)

        if profile is None:
            return None

        profile.allergies = [
            allergy
            for allergy in profile.allergies
            if allergy.id != allergy_id
        ]

        return profile

    # =========================
    # FAMILY MEMBERS
    # =========================

    def add_family_member(
        self,
        parent_profile_id: int,
        member: UserProfile
    ) -> UserProfile | None:

        parent = self.get_user_profile_by_id(parent_profile_id)

        if parent is None:
            return None

        exists = any(
            family_member.profile_id == member.profile_id
            for family_member in parent.family_members
        )

        if exists:
            return parent

        parent.family_members.append(member)

        return parent

    def remove_family_member(
        self,
        parent_profile_id: int,
        member_profile_id: int
    ) -> UserProfile | None:

        parent = self.get_user_profile_by_id(parent_profile_id)

        if parent is None:
            return None

        parent.family_members = [
            member
            for member in parent.family_members
            if member.profile_id != member_profile_id
        ]

        return parent
