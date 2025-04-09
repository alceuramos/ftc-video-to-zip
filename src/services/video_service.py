import asyncio
import io
import os
import tempfile
import zipfile

import cv2
import numpy as np

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

    def extract_frames_and_upload_zip(
        self, video_content: bytes, video_id: int, user_id: int
    ):
        try:
            # Create a temporary file to store the video
            with tempfile.NamedTemporaryFile(
                suffix=".mp4", delete=False
            ) as temp_video:
                temp_video.write(video_content)
                temp_video_path = temp_video.name

            # Create a temporary directory for frames
            with tempfile.TemporaryDirectory() as temp_dir:
                # Open the video file
                cap = cv2.VideoCapture(temp_video_path)
                frame_count = 0

                # Extract frames
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Save frame as JPEG
                    frame_path = os.path.join(
                        temp_dir, f"frame_{frame_count:04d}.jpg"
                    )
                    cv2.imwrite(frame_path, frame)
                    frame_count += 1

                cap.release()

                # Create zip file in memory
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(
                    zip_buffer, "w", zipfile.ZIP_DEFLATED
                ) as zipf:
                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname)

                # Upload zip to S3
                zip_filename = f"frames/{user_id}/video_{video_id}_frames.zip"
                url = f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{zip_filename}"
                S3StorageService().upload_video_to_s3(
                    zip_buffer.getvalue(), zip_filename
                )

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
        finally:
            # Clean up temporary video file
            if "temp_video_path" in locals():
                os.unlink(temp_video_path)
