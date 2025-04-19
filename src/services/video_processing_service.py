from services.temp_file_service import TempFileService
from services.video_frame_extractor import VideoFrameExtractor
from services.zip_service import ZipService


class VideoProcessingService:

    def __init__(
        self,
        temp_file_service: TempFileService = TempFileService(),
        video_frame_extractor: VideoFrameExtractor = VideoFrameExtractor(
            frame_interval=1,
            max_frames=100,
            quality=85,
        ),
        zip_service: ZipService = ZipService(),
    ):
        self.temp_file_service = temp_file_service
        self.video_frame_extractor = video_frame_extractor
        self.zip_service = zip_service

    def extract_frames_to_zip(self, video_content: bytes) -> bytes:

        with self.temp_file_service.create_temp_video_file(
            video_content
        ) as temp_video_path:
            frames = self.video_frame_extractor.extract_frames(temp_video_path)

            zip_content = self.zip_service.create_zip_from_frames(frames)

            return zip_content
