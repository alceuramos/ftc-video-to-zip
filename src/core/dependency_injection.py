from dependency_injector import containers, providers

from db.postgresql.database import SessionLocal
from repositories.user import UserRepository
from repositories.video import VideoRepository
from services.auth_service import AuthService
from services.user_service import UserService
from services.video_service import VideoService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["api.v1.users", "api.v1.auth", "api.v1.videos"]
    )
    db_session = providers.Singleton(SessionLocal)

    user_repository = providers.Factory(UserRepository, db=db_session)
    user_service = providers.Factory(UserService, user_repository)
    auth_service = providers.Factory(AuthService, user_repository)
    video_repository = providers.Factory(VideoRepository, db=db_session)
    video_service = providers.Factory(VideoService, video_repository)
