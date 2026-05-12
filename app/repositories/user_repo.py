from app.models.user import User

fake_users_db: list[User] = []


class UserRepository:

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        return next(
            (
                u for u in fake_users_db
                if u.email == email
            ),
            None
        )

    @staticmethod
    def get_all_users() -> list[User]:
        return fake_users_db

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        return next(
            (
                u for u in fake_users_db
                if u.id == user_id
            ),
            None
        )

    @staticmethod
    def create_user(user: User) -> User:
        fake_users_db.append(user)
        return user

    @staticmethod
    def count_users() -> int:
        return len(fake_users_db)
