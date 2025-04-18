from core.interfaces.storage_service import StorageServiceInterface
from core.settings import settings
from db.postgresql.interfaces.video import VideoRepositoryInterface


class VideoStorageService:
    def __init__(
        self,
        storage_service: StorageServiceInterface,
        video_repository: VideoRepositoryInterface,
    ):
        self.storage_service = storage_service
        self.video_repository = video_repository

    def upload_to_storage(self, content, filename, video_id: int):
        try:
            self.storage_service.upload_file(content, filename)
            self.video_repository.update_video(
                video_id, **{"status": "uploaded"}
            )
        except Exception as e:
            self.video_repository.update_video(
                video_id, **{"status": "failed"}
            )
            raise e

    def upload_zip_to_storage(
        self, zip_content, user_id: int, video_id: int
    ) -> str:
        zip_filename = f"frames/{user_id}/video_{video_id}_frames.zip"
        url = f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{zip_filename}"
        self.storage_service.upload_file(zip_content, zip_filename)
        return url

    def get_download_url(self, filepath: str) -> str:
        return self.storage_service.get_download_url(filepath)
