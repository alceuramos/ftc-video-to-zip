from abc import ABC, abstractmethod


class StorageServiceInterface(ABC):
    @abstractmethod
    def upload_file(self, file_content: bytes, filename: str) -> None:
        """
        Upload a file to storage.

        Args:
            file_content: Content of the file as bytes
            filename: Name of the file in storage
        """
        pass
