import os
import tempfile
from contextlib import contextmanager
from typing import Generator


class TempFileService:
    @staticmethod
    @contextmanager
    def create_temp_video_file(
        video_content: bytes,
    ) -> Generator[str, None, None]:
        """
        Create a temporary video file and yield its path.

        Args:
            video_content: Video content as bytes

        Yields:
            Path to the temporary video file
        """
        with tempfile.NamedTemporaryFile(
            suffix=".mp4", delete=False
        ) as temp_video:
            temp_video.write(video_content)
            temp_video_path = temp_video.name

        try:
            yield temp_video_path
        finally:
            if os.path.exists(temp_video_path):
                os.unlink(temp_video_path)
