import unittest
from unittest.mock import MagicMock, patch

from schemas.video import Video
from services.video_service import VideoService


@patch("services.video_service.VideoRepositoryInterface")
@patch("services.video_service.StorageServiceInterface")
@patch("services.video_service.VideoProcessingService")
@patch("services.video_service.NotificationService")
def test_save_video(
    MockNotificationService,
    MockVideoProcessingService,
    MockStorageService,
    MockVideoRepository,
):
    # Arrange
    mock_video_repository = MockVideoRepository
    mock_storage_service = MockStorageService
    mock_processing_service = MockVideoProcessingService
    mock_notification_service = MockNotificationService

    video_service = VideoService(
        video_repository=mock_video_repository,
        storage_service=mock_storage_service,
    )

    file = MagicMock()
    file.filename = "test_video.mp4"
    user_id = 1
    expected_url = "https://bucket_name.s3.amazonaws.com/test_video.mp4"

    # Create a mock Video instance with required fields
    mock_video_repository.add.return_value = Video(
        id=1,
        file_path=expected_url,
        user_id=user_id,
        title=file.filename,
        status="processing",
    )

    # Act
    saved_video = video_service.save_video(file, file.filename, user_id)

    # Assert
    assert saved_video.file_path == expected_url
    mock_video_repository.add.assert_called_once()


@patch("services.video_service.VideoStorageService")
@patch("services.video_service.VideoRepositoryInterface")
def test_upload_video(MockVideoRepository, MockVideoStorageService):
    # Arrange
    mock_video_repository = MockVideoRepository
    mock_storage_service = MockVideoStorageService.return_value

    video_service = VideoService(
        video_repository=mock_video_repository,
        storage_service=MagicMock(),
    )

    content = b"some_video_content"
    filename = "test_video.mp4"
    video_id = 1

    # Act
    video_service.upload_video(content, filename, video_id)

    # Assert
    mock_storage_service.upload_to_storage.assert_called_once_with(
        content, filename, video_id
    )


@patch("services.video_service.VideoRepositoryInterface")
@patch("services.video_service.StorageServiceInterface")
@patch("services.video_service.VideoProcessingService")
@patch("services.video_service.NotificationService")
def test_process_video_success(
    MockNotificationService,
    MockVideoProcessingService,
    MockStorageService,
    MockVideoRepository,
):
    # Arrange
    mock_video_repository = MockVideoRepository
    mock_storage_service = MockStorageService
    mock_processing_service = MockVideoProcessingService.return_value
    mock_notification_service = MockNotificationService.return_value

    video_service = VideoService(
        video_repository=mock_video_repository,
        storage_service=mock_storage_service,
    )

    # Mock the VideoStorageService instance
    mock_video_storage = MagicMock()
    mock_video_storage.upload_zip_to_storage.return_value = "zip_url"
    video_service.storage_service = mock_video_storage

    video_content = b"some_video_content"
    user = {"id": 1}
    video = Video(
        id=1,
        file_path="some_path",
        user_id=user["id"],
        title="Test Video",
        status="processing",
    )

    mock_processing_service.extract_frames_to_zip.return_value = b"zip_content"

    # Act
    video_service.process_video(video_content, video, user)

    # Assert
    mock_processing_service.extract_frames_to_zip.assert_called_once_with(
        video_content
    )
    mock_video_storage.upload_zip_to_storage.assert_called_once_with(
        b"zip_content", user["id"], video.id
    )
    mock_video_repository.update_video.assert_called_once_with(
        video.id, **{"status": "frames_extracted", "zip_path": "zip_url"}
    )


@patch("services.video_service.VideoRepositoryInterface")
@patch("services.video_service.StorageServiceInterface")
@patch("services.video_service.VideoProcessingService")
@patch("services.video_service.NotificationService")
def test_process_video_failure(
    MockNotificationService,
    MockVideoProcessingService,
    MockStorageService,
    MockVideoRepository,
):
    # Arrange
    mock_video_repository = MockVideoRepository
    mock_storage_service = MockStorageService
    mock_processing_service = MockVideoProcessingService.return_value
    mock_notification_service = MockNotificationService.return_value

    video_service = VideoService(
        video_repository=mock_video_repository,
        storage_service=mock_storage_service,
    )
    video_service.notification_service = mock_notification_service

    video_content = b"some_video_content"
    user = {"id": 1}
    video = Video(
        id=1,
        file_path="some_path",
        user_id=user["id"],
        title="Test Video",
        status="processing",
    )

    mock_processing_service.extract_frames_to_zip.side_effect = Exception(
        "Processing error"
    )

    # Act & Assert
    with unittest.TestCase().assertRaises(Exception):
        video_service.process_video(video_content, video, user)

    mock_video_repository.update_video.assert_called_once_with(
        video.id, **{"status": "frame_extraction_failed"}
    )
    mock_notification_service.send.assert_called_once_with(user, video)


@patch("services.video_service.VideoRepositoryInterface")
def test_list_videos(MockVideoRepository):
    # Arrange
    mock_video_repository = MockVideoRepository

    video_service = VideoService(
        video_repository=mock_video_repository,
        storage_service=MagicMock(),  # Mock storage service as it's not needed for this test
    )

    user_id = 1
    limit = 10
    page = 1
    expected_videos = [
        Video(
            id=1,
            file_path="path1",
            user_id=user_id,
            title="Video 1",
            status="available",
        ),
        Video(
            id=2,
            file_path="path2",
            user_id=user_id,
            title="Video 2",
            status="available",
        ),
    ]
    mock_video_repository.list_videos.return_value = expected_videos

    # Act
    videos = video_service.list_videos(user_id, limit, page)

    # Assert
    assert videos == expected_videos
    mock_video_repository.list_videos.assert_called_once_with(
        user_id, limit, page - 1
    )
