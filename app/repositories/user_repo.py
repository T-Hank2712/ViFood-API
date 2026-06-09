from app.models.user import User


class UserRepository:

    def __init__(self, db):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return next(
            (u for u in self.db.users if u.email == email),
            None
        )

    def get_all_users(self) -> list[User]:
        return self.db.users

    def get_user_by_id(self, user_id: int) -> User | None:
        return next(
            (u for u in self.db.users if u.id == user_id),
            None
        )

    def create_user(self, user: User) -> User:
        self.db.users.append(user)
        return user

    def count_users(self) -> int:
        return len(self.db.users)
