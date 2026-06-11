from app.models.user_profile import UserProfile
from app.models.health_goal import HealthGoal
from app.models.disease import Disease
from app.models.allergy import Allergy
from app.repositories.base_repo import BaseRepository
from app.helpers.convert_time import to_vn_time

from app.schemas.update_profile import UpdateProfileRequest


class UserProfileRepository(BaseRepository):
    
    def __init__(self, db):
        super().__init__(db)

    # =========================
    # BASIC
    # =========================
    
    def _map_profile(self, record) -> UserProfile:
        p = record["p"]

        return UserProfile(
            profile_id=p.get("id"),
            first_name=p.get("firstName"),
            last_name=p.get("lastName"),
            avatar=p.get("avatar"),
            created_at=to_vn_time(p.get("createdAt")),
            updated_at=to_vn_time(p.get("updatedAt")),
        )
        
    def _map_profile_with_relations(self, record):
        p = record["p"]
        return {
            "profile_id": p.get("id"),
            "first_name": p.get("firstName"),
            "last_name": p.get("lastName"),
            "avatar": p.get("avatar"),
            "health_goals": p.get("health_goals", []),
            "diseases": p.get("diseases", []),
            "allergies": p.get("allergies", [])
        }
        
    def create_profile(self, user_id: str, profile: UserProfile):

        profile_data = self.prepare_entity({
            "firstName": profile.first_name,
            "lastName": profile.last_name,
            "avatar": profile.avatar,
        })
        
        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})
                CREATE (p:Profile $profile)
                CREATE (u)-[:HAS_FAMILY_MEMBER]->(p)
                RETURN p
            """, {
                "user_id": user_id,
                "profile": profile_data
            }).single()

            if not result:
                return None

            return self._map_profile(result)

        return self.write(query)

    def get_user_profile_by_user_id(self, user_id: str) -> UserProfile | None:

        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})
                MATCH (u)-[:HAS_PROFILE]->(p:Profile)
                RETURN p
                LIMIT 1
            """, {
                "user_id": user_id
            })

            record = result.single()

            if not record:
                return None

            return self._map_profile(record)

        return self.read(query)
    
    def get_profile_by_user_access(self, user_id: str, profile_id: str) -> UserProfile:
    
        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})
                MATCH (u)-[:HAS_PROFILE|HAS_FAMILY_MEMBER]->(p:Profile {id: $profile_id})
                RETURN p
                LIMIT 1
            """, {
                "user_id": user_id,
                "profile_id": profile_id
            })

            record = result.single()

            if not record:
                return None

            return self._map_profile(record)

        return self.read(query)
    
    def update_user_profile(self, user_id: str, profile_id: str, profile: UpdateProfileRequest) -> UserProfile | None:
        
        profile_data = self.prepare_update_entity({
            "firstName": profile.first_name,
            "lastName": profile.last_name,
            "avatar": profile.avatar
        })
        
        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})-[:HAS_PROFILE|HAS_FAMILY_MEMBER]->(p:Profile {id: $profile_id})
                
                SET p += $profile_data
                    
                RETURN p
                LIMIT 1
                """, {
                    "user_id": user_id,
                    "profile_id": profile_id,
                    "profile_data": profile_data,
                })
            record = result.single()

            if not record:
                return None

            return self._map_profile(record)

        return self.write(query)
    
    def delete_family_member(self, user_id: str, profile_id: str) -> bool:
        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})-[:HAS_FAMILY_MEMBER]->(p:Profile {id: $profile_id})
                DETACH DELETE p
                RETURN count(*) > 0 AS deleted
                """, {
                    "user_id": user_id,
                    "profile_id": profile_id,
                })
            record = result.single()

            return record["deleted"]

        return self.write(query)

    # def update_user_profile(
    #     self,
    #     profile_id: int,
    #     first_name: str,
    #     last_name: str,
    #     avatar: str | None = None
    # ) -> UserProfile | None:

    #     profile = self.get_user_profile_by_id(profile_id)

    #     if profile is None:
    #         return None

    #     profile.first_name = first_name
    #     profile.last_name = last_name

    #     if avatar is not None:
    #         profile.avatar = avatar

    #     return profile

    # def delete_user_profile(
    #     self,
    #     profile_id: int
    # ) -> UserProfile:

    #     profile = self.get_user_profile_by_id(profile_id)

    #     if profile is None:
    #         return False

    #     # Nếu là family member thì remove khỏi parent
    #     if profile.parent_profile_id is not None:
    #         parent = self.get_user_profile_by_id(profile.parent_profile_id)

    #         if parent is not None:
    #             parent.family_members = [
    #                 member
    #                 for member in parent.family_members
    #                 if member.profile_id != profile_id
    #             ]

    #     self.db.user_profiles.remove(profile)
        
    #     return parent.family_members if parent else []

    # def delete_family_member_profile(
    #     self,
    #     member_profile_id: int
    # ) -> bool:

    #     member = self.get_user_profile_by_id(member_profile_id)

    #     if member is None:
    #         return False

    #     # Tìm parent và remove khỏi danh sách family members
    #     if member.parent_profile_id is not None:
    #         parent = self.get_user_profile_by_id(member.parent_profile_id)

    #         if parent is not None:
    #             parent.family_members = [
    #                 family_member
    #                 for family_member in parent.family_members
    #                 if family_member.profile_id != member_profile_id
    #             ]

    #     # Xóa profile khỏi database
    #     self.db.user_profiles.remove(member)

    #     return True

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
            raise ValueError("Health goal already exists")

        profile.health_goals.append(health_goal)

        return profile.health_goals

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

        return profile.health_goals

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
            raise ValueError("Disease already exists")

        profile.diseases.append(disease)

        return profile.diseases

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

        return profile.diseases

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
            raise ValueError("Allergy already exists")

        profile.allergies.append(allergy)

        return profile.allergies

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

        return profile.allergies

    # =========================
    # FAMILY MEMBERS
    # =========================
    
    def get_family_members(self, user_id: str) -> list[UserProfile]:
        
        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})-[:HAS_FAMILY_MEMBER]->(p:Profile)
                RETURN p
            """, {
                "user_id": user_id
            })

            return [self._map_profile(r) for r in result]

        return self.read(query)
