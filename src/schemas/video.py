from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class VideoInput(BaseModel):
    title: str = Field(..., example="My Video")
    file_path: str = Field(..., example="/path/to/video.mp4")
    status: str | None = Field("processing", example="processing")
    user_id: int = Field(..., example="user_id")


class Video(BaseModel):
    title: str = Field(..., example="My Video")
    file_path: str = Field(..., example="/path/to/video.mp4")
    zip_path: str | None = Field(
        None,
        example="https://s3.amazonaws.com/bucket/user_id/video_id_frames.zip",
    )
    status: str | None = Field("processing", example="processing")
    user_id: int = Field(..., example="user_id")
    created_at: datetime | None = None
    updated_at: datetime | None = None
    id: int | None = None

    model_config = ConfigDict(extra="ignore", from_attributes=True)

class ItemType(str, Enum):
    video = "video"
    zip = "zip"
