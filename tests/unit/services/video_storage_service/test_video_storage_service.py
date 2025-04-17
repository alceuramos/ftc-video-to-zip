from unittest.mock import Mock, patch

import pytest

from src.core.settings import settings
from src.services.video_storage_service import VideoStorageService


@pytest.fixture
def storage_service_mock():
    return Mock()


@pytest.fixture
def video_repository_mock():
    return Mock()


@pytest.fixture
def video_storage_service(storage_service_mock, video_repository_mock):
    return VideoStorageService(
        storage_service=storage_service_mock,
        video_repository=video_repository_mock,
    )


def test_upload_to_storage_success(
    video_storage_service, storage_service_mock, video_repository_mock
):
    content = b"test content"
    filename = "test.mp4"
    video_id = 1

    video_storage_service.upload_to_storage(content, filename, video_id)

    storage_service_mock.upload_file.assert_called_once_with(content, filename)
    video_repository_mock.update_video.assert_called_once_with(
        video_id, status="uploaded"
    )


def test_upload_to_storage_failure(
    video_storage_service, storage_service_mock, video_repository_mock
):
    content = b"test content"
    filename = "test.mp4"
    video_id = 1
    storage_service_mock.upload_file.side_effect = Exception("Upload failed")

    with pytest.raises(Exception) as exc_info:
        video_storage_service.upload_to_storage(content, filename, video_id)

    assert str(exc_info.value) == "Upload failed"
    storage_service_mock.upload_file.assert_called_once_with(content, filename)
    video_repository_mock.update_video.assert_called_once_with(
        video_id, status="failed"
    )


def test_upload_zip_to_storage(video_storage_service, storage_service_mock):
    zip_content = b"zip content"
    user_id = 1
    video_id = 1
    expected_filename = f"frames/{user_id}/video_{video_id}_frames.zip"
    expected_url = f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{expected_filename}"

    result = video_storage_service.upload_zip_to_storage(
        zip_content, user_id, video_id
    )

    assert result == expected_url
    storage_service_mock.upload_file.assert_called_once_with(
        zip_content, expected_filename
    )
