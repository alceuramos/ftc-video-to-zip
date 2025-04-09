import asyncio

from core.settings import settings
from core.video_upload_s3 import S3StorageService
from db.postgresql.interfaces.video import VideoRepositoryInterface
from schemas.video import Video, VideoInput


class VideoService:
    def __init__(self, video_repository: VideoRepositoryInterface):
        self.video_repository: VideoRepositoryInterface = video_repository

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

    def upload_to_s3(self, content, filename, video_id: int):
        try:

            S3StorageService().upload_video_to_s3(content, filename)
            self.video_repository.update_video(
                video_id, **{"status": "uploaded"}
            )
        except Exception as e:
            self.video_repository.update_video(
                video_id, **{"status": "failed"}
            )
            raise e
