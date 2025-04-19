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
        self.frame_interval = frame_interval
        self.max_frames = max_frames
        self.quality = quality

    def extract_frames(
        self, video_path: str
    ) -> Generator[Tuple[int, bytes], None, None]:

        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        extracted_count = 0

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps > 0:

            self.frame_interval = max(1, int(fps))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % self.frame_interval != 0:
                frame_count += 1
                continue

            encode_params = [cv2.IMWRITE_JPEG_QUALITY, self.quality]
            _, buffer = cv2.imencode(".jpg", frame, encode_params)
            frame_bytes = buffer.tobytes()

            yield extracted_count, frame_bytes
            extracted_count += 1
            frame_count += 1

            if (
                self.max_frames is not None
                and extracted_count >= self.max_frames
            ):
                break

        cap.release()
