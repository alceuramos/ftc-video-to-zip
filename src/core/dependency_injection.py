from dependency_injector import containers, providers

from db.postgresql.database import SessionLocal
from infrastructure.storage.s3_storage_service import S3StorageService
from repositories.user import UserRepository
from repositories.video import VideoRepository
from services.auth_service import AuthService
from services.notification_service import NotificationService
from services.user_service import UserService
from services.video_processing_service import VideoProcessingService
from services.video_service import VideoService
from services.video_storage_service import VideoStorageService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["api.v1.users", "api.v1.auth", "api.v1.videos"]
    )
    db_session = providers.Singleton(SessionLocal)

    # Repositories
    user_repository = providers.Factory(UserRepository, db=db_session)
    video_repository = providers.Factory(VideoRepository, db=db_session)

    # Services
    storage_service = providers.Singleton(S3StorageService)
    video_storage_service = providers.Factory(
        VideoStorageService,
        storage_service=storage_service,
        video_repository=video_repository,
    )
    video_processing_service = providers.Factory(VideoProcessingService)
    notification_service = providers.Factory(NotificationService)

    # Main services used by API
    user_service = providers.Factory(
        UserService, user_repository=user_repository
    )
    auth_service = providers.Factory(
        AuthService, user_repository=user_repository
    )
    video_service = providers.Factory(
        VideoService,
        video_repository=video_repository,
        storage_service=storage_service,
    )
