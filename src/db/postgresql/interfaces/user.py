import abc

from schemas.user import User, UserCredentials, UserInput


class UserRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def add(self, user: UserInput) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, user_id: str) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    def validate_credentials(
        self, user_credentials: UserCredentials
    ) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    def list_users(self, limit: int, offset: int) -> list[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_user(self, user: User) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def update_user(self, user_id: int, **kwargs) -> User:
        raise NotImplementedError
