from unittest.mock import MagicMock

import pytest
from fastapi import UploadFile

from api.v1.validations.videos import check_video_size, check_video_type


def test_check_video_size_valid():
    # Arrange
    mock_file = MagicMock(spec=UploadFile)
    mock_file.size = 5 * 1024 * 1024  # 5 MB

    # Act
    result = check_video_size(mock_file)

    # Assert
    assert result is True


def test_check_video_size_invalid():
    # Arrange
    mock_file = MagicMock(spec=UploadFile)
    mock_file.size = 15 * 1024 * 1024  # 15 MB

    # Act
    result = check_video_size(mock_file)

    # Assert
    assert result is False


def test_check_video_type_valid():
    # Arrange
    mock_file = MagicMock(spec=UploadFile)
    mock_file.content_type = "video/mp4"

    # Act
    result = check_video_type(mock_file)

    # Assert
    assert result is True


def test_check_video_type_invalid():
    # Arrange
    mock_file = MagicMock(spec=UploadFile)
    mock_file.content_type = "image/jpeg"

    # Act
    result = check_video_type(mock_file)

    # Assert
    assert result is False
