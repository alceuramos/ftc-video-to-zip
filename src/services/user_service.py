from db.postgresql.interfaces.user import UserRepositoryInterface
from src.core.security import hash_password
from src.schemas.user import User, UserInput, UserUpdate

EMAIL_ALREADY_USED_ERROR = "Email already used"


class UserService:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository: UserRepositoryInterface = user_repository

    def create_user(self, user: UserInput) -> User:
        hashed_password = hash_password(user.password)
        user.password = hashed_password
        existing_user = self.user_repository.get_by_email(user.email)
        if existing_user:
            raise ValueError(EMAIL_ALREADY_USED_ERROR)
        return self.user_repository.add(user)

    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repository.get_by_email(email)

    def is_user_authenticated(self, email: str, password: str) -> bool:
        hashed_password = hash_password(password)
        user = self.user_repository.validate_credentials(
            email, hashed_password
        )
        return bool(user)

    def list_users(self, limit: int, page: int) -> list[User]:
        return self.user_repository.list_users(limit, page - 1)

    def update_user(self, user_id: int, user_data: UserUpdate):
        user = self.user_repository.get_by_id(user_id)
        if user:
            self.user_repository.update_user(
                user_id, **user_data.model_dump(exclude_unset=True)
            )
        return user

    def delete_user(self, user_id: str):
        user = self.user_repository.get_by_id(user_id)
        if user:
            self.user_repository.delete_user(user)
        return user
