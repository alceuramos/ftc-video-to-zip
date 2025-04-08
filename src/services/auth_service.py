from datetime import UTC, datetime, timedelta

from core.security import encode_jwt, hash_password
from core.settings import get_settings
from db.postgresql.interfaces.user import UserRepositoryInterface
from schemas.token import Token
from schemas.user import UserCredentials

settings = get_settings()


class AuthService:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository: UserRepositoryInterface = user_repository

    def login(
        self,
        user_credentials: UserCredentials,
    ) -> Token | None:
        user_credentials.password = hash_password(user_credentials.password)

        user = self.user_repository.validate_credentials(user_credentials)
        if not user:
            return None
        expiration_time = datetime.now(tz=UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        token_data = {
            "sub": user.email,
            "is_admin": user.is_admin,
            "is_reader": user.is_reader,
            "is_editor": user.is_editor,
            "exp": expiration_time,
            "id": user.id,
        }
        token = encode_jwt(token_data)
        return Token(access_token=token, token_type="bearer")
