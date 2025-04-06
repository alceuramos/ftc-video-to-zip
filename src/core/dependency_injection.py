from dependency_injector import containers, providers

from db.postgresql.database import SessionLocal
from repositories.user import UserRepository
from services.auth_service import AuthService
from services.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["api.v1.users", "api.v1.auth"]
    )
    db_session = providers.Singleton(SessionLocal)

    user_repository = providers.Factory(UserRepository, db=db_session)
    user_service = providers.Factory(UserService, user_repository)
    auth_service = providers.Factory(AuthService, user_repository)
