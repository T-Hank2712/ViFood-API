from app.models.user_profile import UserProfile
from app.models.health_goal import HealthGoal
from app.models.disease import Disease
from app.models.allergy import Allergy
from app.repositories.base_repo import BaseRepository
from app.helpers.convert_time import to_vn_time

from app.schemas.update_profile import UpdateProfileRequest

from app.repositories.health_goal_repo import HealthGoalRepository
from app.repositories.disease_repo import DiseaseRepository


class UserProfileRepository(BaseRepository):
    
    def __init__(self, db):
        super().__init__(db)
        self.health_goal_repo = HealthGoalRepository(db)
        self.disease_repo = DiseaseRepository(db)

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

    # =========================
    # HEALTH GOALS
    # =========================

    def get_health_goals_by_profile_id(
        self,
        profile_id: str
    ) -> list[HealthGoal]:

        def query(tx):
            result = tx.run("""
                MATCH (p:Profile {id: $profile_id})
                    -[:HAS_HEALTH_GOAL]->(h:HealthGoal)
                RETURN h
            """, {
                "profile_id": profile_id
            })

            return [
                self.health_goal_repo._map_health_goal(record)
                for record in result
            ]

        return self.read(query)

    def add_health_goal_to_profile(
        self,
        profile_id: str,
        health_goal_id: str
    ) -> bool:
        def query(tx):
            result = tx.run("""
                MATCH (p:Profile {id: $profile_id})
                MATCH (h:HealthGoal {id: $health_goal_id})

                MERGE (p)-[:HAS_HEALTH_GOAL]->(h)

                RETURN COUNT(h) > 0 AS success
            """, {
                "profile_id": profile_id,
                "health_goal_id": health_goal_id
            })

            record = result.single()
            return record["success"] if record else False

        return self.write(query)
    
    def remove_health_goal_from_profile(
        self,
        profile_id: str,
        health_goal_id: str
    ) -> bool:
        def query(tx):
            result = tx.run("""
                MATCH (p:Profile {id: $profile_id})
                    -[r:HAS_HEALTH_GOAL]->
                    (h:HealthGoal {id: $health_goal_id})

                DELETE r

                RETURN COUNT(r) > 0 AS success
            """, {
                "profile_id": profile_id,
                "health_goal_id": health_goal_id
            })

            record = result.single()
            return record["success"] if record else False

        return self.write(query)

    # # =========================
    # # DISEASES
    # # =========================

    def get_diseases_by_profile_id(
        self,
        profile_id: str
    ) -> list[Disease]:

        def query(tx):
            result = tx.run("""
                MATCH (p:Profile {id: $profile_id})
                    -[:HAS_DISEASE]->(d:Disease)
                RETURN d
            """, {
                "profile_id": profile_id
            })

            return [
                self.disease_repo._map_disease(record)
                for record in result
            ]

        return self.read(query)

    def add_disease_to_profile(
        self,
        profile_id: str,
        disease_id: str
    ) -> bool:
        def query(tx):
            result = tx.run("""
                MATCH (p:Profile {id: $profile_id})
                MATCH (d:Disease {id: $disease_id})

                MERGE (p)-[:HAS_DISEASE]->(d)

                RETURN COUNT(d) > 0 AS success
            """, {
                "profile_id": profile_id,
                "disease_id": disease_id
            })

            record = result.single()
            return record["success"] if record else False

        return self.write(query)

    def remove_disease_from_profile(
        self,
        profile_id: str,
        disease_id: str
    ) -> bool:
        def query(tx):
            result = tx.run("""
                MATCH (p:Profile {id: $profile_id})
                    -[r:HAS_DISEASE]->
                    (d:Disease {id: $disease_id})

                DELETE r

                RETURN COUNT(r) > 0 AS success
            """, {
                "profile_id": profile_id,
                "disease_id": disease_id
            })

            record = result.single()
            return record["success"] if record else False

        return self.write(query)

    # # =========================
    # # ALLERGIES
    # # =========================

    def get_allergies_by_profile_id(
        self,
        profile_id: str
    ) -> list[Allergy]:

        def query(tx):
            result = tx.run("""
                MATCH (p:Profile {id: $profile_id})
                    -[:HAS_ALLERGY]->(a:Allergy)
                RETURN a
            """, {
                "profile_id": profile_id
            })

            return [
                self.allergy_repo._map_allergy(record)
                for record in result
            ]

        return self.read(query)

    def add_allergy_to_profile(
        self,
        profile_id: str,
        allergy_id: str
    ) -> bool:
        def query(tx):
            result = tx.run("""
                MATCH (p:Profile {id: $profile_id})
                MATCH (a:Allergy {id: $allergy_id})

                MERGE (p)-[:HAS_ALLERGY]->(a)

                RETURN COUNT(a) > 0 AS success
            """, {
                "profile_id": profile_id,
                "allergy_id": allergy_id
            })

            record = result.single()
            return record["success"] if record else False

        return self.write(query)

    def remove_allergy_from_profile(
        self,
        profile_id: str,
        allergy_id: str
    ) -> bool:
        def query(tx):
            result = tx.run("""
                MATCH (p:Profile {id: $profile_id})
                    -[r:HAS_ALLERGY]->
                    (a:Allergy {id: $allergy_id})

                DELETE r

                RETURN COUNT(r) > 0 AS success
            """, {
                "profile_id": profile_id,
                "allergy_id": allergy_id
            })

            record = result.single()
            return record["success"] if record else False

        return self.write(query)

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
