import os
import tempfile
from typing import Generator, Optional, Tuple

import cv2


class VideoFrameExtractor:
    def __init__(
        self,
        frame_interval: int = 1,
        max_frames: Optional[int] = None,
        quality: int = 90,
    ):
        """
        Initialize the frame extractor with extraction parameters.

        Args:
            frame_interval: Extract every nth frame (default: 1, meaning all frames)
            max_frames: Maximum number of frames to extract (default: None, meaning no limit)
            quality: JPEG quality (1-100, higher means better quality but larger file size)
        """
        self.frame_interval = frame_interval
        self.max_frames = max_frames
        self.quality = quality

    def extract_frames(
        self, video_path: str
    ) -> Generator[Tuple[int, bytes], None, None]:
        """
        Extract frames from a video file and yield them as JPEG bytes.

        Args:
            video_path: Path to the video file

        Yields:
            Tuple containing frame number and frame data as JPEG bytes
        """
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        extracted_count = 0

        # Get total frames and fps for better control
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Calculate frame interval based on desired frames per second
        if fps > 0:
            # If we want 1 frame per second, we need to skip (fps - 1) frames
            # This ensures we get a good representation of the video
            self.frame_interval = max(1, int(fps))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Skip frames based on interval
            if frame_count % self.frame_interval != 0:
                frame_count += 1
                continue

            # Convert frame to JPEG bytes with specified quality
            encode_params = [cv2.IMWRITE_JPEG_QUALITY, self.quality]
            _, buffer = cv2.imencode(".jpg", frame, encode_params)
            frame_bytes = buffer.tobytes()

            yield extracted_count, frame_bytes
            extracted_count += 1
            frame_count += 1

            # Check if we've reached the maximum number of frames
            if (
                self.max_frames is not None
                and extracted_count >= self.max_frames
            ):
                break

        cap.release()
