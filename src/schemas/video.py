from datetime import datetime

from pydantic import BaseModel, Field


class Video(BaseModel):
    title: str = Field(..., example="My Video")
    file_path: str = Field(..., example="/path/to/video.mp4")
    zip_path: str | None = Field(
        None, example="/path/to/images-from-video.zip"
    )
    status: str | None = Field("processing", example="processing")
    user_id: int = Field(..., example="user_id")
    created_at: datetime | None = None
    updated_at: datetime | None = None
