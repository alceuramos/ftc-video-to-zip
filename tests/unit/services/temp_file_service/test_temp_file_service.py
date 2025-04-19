import os
import unittest

from src.services.temp_file_service import TempFileService


def test_create_temp_video_file():
    video_content = b"This is a test video content."

    with TempFileService.create_temp_video_file(
        video_content
    ) as temp_file_path:
        assert os.path.exists(temp_file_path)
        with open(temp_file_path, "rb") as f:
            content = f.read()
            assert content == video_content

    assert not os.path.exists(temp_file_path)
