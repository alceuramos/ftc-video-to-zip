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

    @abstractmethod
    def get_download_url(self, filepath: str) -> str:
        """
        Get a pre-signed URL for downloading a file.

        Args:
            filename: The name of the file in storage.

        Returns:
            A pre-signed URL for the file.
        """
        pass
