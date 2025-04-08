import abc

from schemas.video import Video, VideoInput


class VideoRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def add(self, video: VideoInput) -> Video:
        raise NotImplementedError
