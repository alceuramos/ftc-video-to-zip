import unittest
from unittest.mock import patch

from services.video_processing_service import VideoProcessingService


@patch("services.video_processing_service.TempFileService")
@patch("services.video_processing_service.VideoFrameExtractor")
@patch("services.video_processing_service.ZipService")
def test_extract_frames_to_zip(
    MockZipService, MockVideoFrameExtractor, MockTempFileService
):
    mock_temp_file_service = MockTempFileService.return_value
    mock_video_frame_extractor = MockVideoFrameExtractor.return_value
    mock_zip_service = MockZipService.return_value

    mock_temp_file_service.create_temp_video_file.return_value.__enter__.return_value = (
        "temp_video_path"
    )
    mock_video_frame_extractor.extract_frames.return_value = [
        "frame1",
        "frame2",
    ]
    mock_zip_service.create_zip_from_frames.return_value = b"zip_content"

    video_processing_service = VideoProcessingService(
        temp_file_service=mock_temp_file_service,
        video_frame_extractor=mock_video_frame_extractor,
        zip_service=mock_zip_service,
    )

    video_content = b"some_video_content"

    result = video_processing_service.extract_frames_to_zip(video_content)

    mock_temp_file_service.create_temp_video_file.assert_called_once_with(
        video_content
    )
    mock_video_frame_extractor.extract_frames.assert_called_once_with(
        "temp_video_path"
    )
    mock_zip_service.create_zip_from_frames.assert_called_once_with(
        ["frame1", "frame2"]
    )
    assert result == b"zip_content"
