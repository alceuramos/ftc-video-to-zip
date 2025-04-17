import unittest
from unittest.mock import patch

import numpy as np

from services.video_frame_extractor import VideoFrameExtractor


@patch("cv2.VideoCapture")
def test_extract_frames(MockVideoCapture):
    mock_cap = MockVideoCapture.return_value
    mock_cap.get.side_effect = [10, 1]

    dummy_frame = np.zeros((100, 100, 3), dtype=np.uint8)
    mock_cap.read.side_effect = [(True, dummy_frame) for _ in range(10)] + [
        (False, None)
    ]

    extractor = VideoFrameExtractor(frame_interval=1, max_frames=5, quality=90)

    frames = list(extractor.extract_frames("dummy_video_path"))

    assert len(frames) == 5
    for i, (index, frame_bytes) in enumerate(frames):
        assert index == i
        assert isinstance(frame_bytes, bytes)

    mock_cap.release.assert_called_once()
