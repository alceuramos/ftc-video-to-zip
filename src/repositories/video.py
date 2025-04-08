from datetime import datetime

from sqlalchemy.orm import Session

from src.db.postgresql.interfaces.video import VideoRepositoryInterface
from src.db.postgresql.models.video import Video as VideoDB
from src.schemas.video import Video, VideoInput


class VideoRepository(VideoRepositoryInterface):
    def __init__(self, db: Session):
        self.db: Session = db

    def add(self, video: VideoInput) -> Video:
        now = datetime.now()
        db_video = VideoDB(
            title=video.title,
            file_path=video.file_path,
            user_id=video.user_id,
            created_at=now,
            updated_at=now,
        )

        self.db.add(db_video)
        self.db.commit()
        self.db.refresh(db_video)
        video = Video.model_validate(db_video)
        return video
