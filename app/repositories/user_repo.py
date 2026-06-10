from app.models.user import User
from app.models.user_profile import UserProfile
from app.repositories.base_repo import BaseRepository
from app.helpers.id_generator import generate_id


class UserRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)
        
    def _map_user(self, record) -> User:
        u = record["u"]
        return User(
            id=u.get("id"),
            email=u.get("email"),
            password_hash=u.get("passwordHash"),
            is_active=u.get("isActive"),
            created_at=u.get("createdAt"),
            updated_at=u.get("updatedAt"),
        )

    def _map_user_with_profile(self, record):
        u = record["u"]
        p = record["p"]

        user_data = {
            "user_id": u.get("id"),
            "email": u.get("email"),
            "is_active": u.get("isActive"),
            "created_at": u.get("createdAt"),
            "updated_at": u.get("updatedAt"),
        }

        profile_data = None
        if p:
            profile_data = {
                "profile_id": p.get("id"),
                "first_name": p.get("firstName"),
                "last_name": p.get("lastName"),
                "avatar": p.get("avatar"),
            }

        return {
            "user": user_data,
            "profile": profile_data
        }

    def get_user_by_email(self, email: str):

        def query(tx):
            result = tx.run("""
                MATCH (u:User)
                WHERE u.email = $email
                RETURN u
                LIMIT 1
            """, {"email": email}).single()

            if not result:
                return None

            return self._map_user(result)

        return self.read(query)

    def get_user_by_id(self, user_id: str):
        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $id})
                RETURN u
                LIMIT 1
            """, {"id": user_id}).single()

            if not result:
                return None

            return dict(result["u"])

        return self.read(query)

    def get_all_users(self):

        def query(tx):
            result = tx.run("""
                MATCH (u:User)
                RETURN u
            """)

            return [dict(r["u"]) for r in result]

        return self.read(query)

    def create_user(self, user: User, user_profile: UserProfile):

        user_data = self.prepare_entity({
            "id": generate_id(),
            "email": user.email,
            "passwordHash": user.password_hash,
            "isActive": user.is_active,
        })

        profile_data = self.prepare_entity({
            "id": generate_id(),
            "firstName": user_profile.first_name,
            "lastName": user_profile.last_name,
            "avatar": user_profile.avatar,
        })

        def query(tx):
            result = tx.run("""
                CREATE (u:User $user)
                CREATE (p:Profile $profile)
                CREATE (u)-[:HAS_PROFILE]->(p)
                RETURN u
            """, {
                "user": user_data,
                "profile": profile_data
            }).single()

            if not result:
                return None

            return self._map_user(result)

        return self.write(query)

    def count_users(self):
        def query(tx):
            result = tx.run("""
                MATCH (u:User)
                RETURN count(u) AS total
            """).single()

            return result["total"]

        return self.read(query)

    def get_current_user(self, user_id: str):

        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})
                OPTIONAL MATCH (u)-[:HAS_PROFILE]->(p:Profile)
                RETURN u, p
            """, {"user_id": user_id}).single()

            if not result:
                return None

            return self._map_user_with_profile(result)

        return self.read(query)
