import abc

from schemas.video import Video, VideoInput


class VideoRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def add(self, video: VideoInput) -> Video:
        raise NotImplementedError

    @abc.abstractmethod
    def update_video(self, video_id: int, **kwargs) -> Video:
        raise NotImplementedError

    @abc.abstractmethod
    def list_videos(
        self, user_id: int, limit: int, offset: int
    ) -> list[Video]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, video_id: int) -> Video:
        raise NotImplementedError
