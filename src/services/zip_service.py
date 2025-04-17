import io
import zipfile
from typing import Generator, Tuple


class ZipService:
    @staticmethod
    def create_zip_from_frames(
        frames: Generator[Tuple[int, bytes], None, None],
    ) -> bytes:

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for frame_count, frame_bytes in frames:
                frame_name = f"frame_{frame_count:04d}.jpg"
                zipf.writestr(frame_name, frame_bytes)

        return zip_buffer.getvalue()
