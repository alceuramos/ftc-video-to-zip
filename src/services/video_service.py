import asyncio
import io
import os
import tempfile
import zipfile
from typing import Generator, Tuple

import cv2
import numpy as np
from core.interfaces.storage_service import StorageServiceInterface
from core.settings import settings
from db.postgresql.interfaces.video import VideoRepositoryInterface
from schemas.video import Video, VideoInput
from services.temp_file_service import TempFileService
from services.video_frame_extractor import VideoFrameExtractor
from services.zip_service import ZipService


class VideoService:
    def __init__(
        self,
        video_repository: VideoRepositoryInterface,
        storage_service: StorageServiceInterface,
        temp_file_service: TempFileService = TempFileService(),
        video_frame_extractor: VideoFrameExtractor = VideoFrameExtractor(
            frame_interval=1,  # Extract every frame
            max_frames=100,  # Maximum 100 frames
            quality=85,  # Good quality with reasonable file size
        ),
        zip_service: ZipService = ZipService(),
    ):
        self.video_repository: VideoRepositoryInterface = video_repository
        self.storage_service = storage_service
        self.temp_file_service = temp_file_service
        self.video_frame_extractor = video_frame_extractor
        self.zip_service = zip_service

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
            self.storage_service.upload_file(content, filename)
            self.video_repository.update_video(
                video_id, **{"status": "uploaded"}
            )
        except Exception as e:
            self.video_repository.update_video(
                video_id, **{"status": "failed"}
            )
            raise e

    def extract_frames_and_upload_zip(
        self, video_content: bytes, video_id: int, user_id: int
    ):
        try:
            with self.temp_file_service.create_temp_video_file(
                video_content
            ) as temp_video_path:
                # Extract frames
                frames = self.video_frame_extractor.extract_frames(
                    temp_video_path
                )

                # Create zip file
                zip_content = self.zip_service.create_zip_from_frames(frames)

                # Upload zip to S3
                zip_filename = f"frames/{user_id}/video_{video_id}_frames.zip"
                url = f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{zip_filename}"
                self.storage_service.upload_file(zip_content, zip_filename)

                # Update video status
                self.video_repository.update_video(
                    video_id,
                    **{"status": "frames_extracted", "zip_path": url},
                )

        except Exception as e:
            self.video_repository.update_video(
                video_id, **{"status": "frame_extraction_failed"}
            )
            raise e

    def list_videos(self, user_id: int, limit: int, page: int) -> list[Video]:
        return self.video_repository.list_videos(user_id, limit, page - 1)
