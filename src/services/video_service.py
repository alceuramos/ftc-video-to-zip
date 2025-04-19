from core.interfaces.storage_service import StorageServiceInterface
from core.settings import settings
from db.postgresql.interfaces.video import VideoRepositoryInterface
from schemas.video import ItemType, Video, VideoInput
from services.exceptions import ItemAccessException, ItemNotFoundException
from services.notification_service import NotificationService
from services.video_processing_service import VideoProcessingService
from services.video_storage_service import VideoStorageService


class VideoService:
    def __init__(
        self,
        video_repository: VideoRepositoryInterface,
        storage_service: StorageServiceInterface,
    ):
        self.video_repository = video_repository
        self.storage_service = VideoStorageService(
            storage_service, video_repository
        )
        self.processing_service = VideoProcessingService()
        self.notification_service = NotificationService()

    def save_video(self, file, filename, user_id: int) -> Video:
        url = f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{filename}"

        video = VideoInput(
            file_path=url,
            user_id=user_id,
            title=file.filename,
            status="processing",
        )
        saved_video = self.video_repository.add(video)

        return saved_video

    def upload_video(self, content, filename, video_id: int):
        self.storage_service.upload_to_storage(content, filename, video_id)

    def process_video(self, video_content: bytes, video: Video, user: dict):
        user_id = user["id"]
        try:
            zip_content = self.processing_service.extract_frames_to_zip(
                video_content
            )

            url = self.storage_service.upload_zip_to_storage(
                zip_content, user_id, video.id
            )

            self.video_repository.update_video(
                video.id,
                **{"status": "frames_extracted", "zip_path": url},
            )
        except Exception as e:
            self.video_repository.update_video(
                video.id, **{"status": "frame_extraction_failed"}
            )

            self.notification_service.send(user, video)
            raise e

    def list_videos(self, user_id: int, limit: int, page: int) -> list[Video]:
        offset = (page - 1) * limit
        return self.video_repository.list_videos(user_id, limit, offset)

    def get_video_download_url(
        self, video_id: str, user_id: int, item_type: ItemType
    ) -> str:
        video = self.video_repository.get(video_id)
        if video is None:
            raise ItemNotFoundException("Video not found.")
        if video.user_id != user_id:
            raise ItemAccessException("Forbidden access to the video.")
        path_options = {
            ItemType.video: video.file_path,
            ItemType.zip: video.zip_path,
        }
        item_path = path_options.get(item_type)
        filepath = self.get_filename(item_path)
        return self.storage_service.get_download_url(filepath)

    @staticmethod
    def get_filename(path: str) -> str:
        return path.split("s3.amazonaws.com/")[1]
