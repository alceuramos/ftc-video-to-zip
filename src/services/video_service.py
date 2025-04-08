from core.settings import settings
from core.video_upload_s3 import S3StorageService
from db.postgresql.interfaces.video import VideoRepositoryInterface
from schemas.video import Video, VideoInput


class VideoService:
    def __init__(self, video_repository: VideoRepositoryInterface):
        self.video_repository: VideoRepositoryInterface = video_repository

    async def save_video(self, file, user_id: int) -> Video:
        contents = await file.read()
        filename = f"videos/{user_id}/{file.filename}"

        S3StorageService().upload_file(
            contents,
            filename,
            file.content_type,
        )
        url = f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{filename}"
        video = VideoInput(
            file_path=url,
            user_id=user_id,
            title=file.filename,
            status="processing",
        )
        return self.video_repository.add(video)
