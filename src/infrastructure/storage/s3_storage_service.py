import io

import boto3

from core.interfaces.storage_service import StorageServiceInterface
from core.settings import settings


class S3StorageService(StorageServiceInterface):
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            aws_account_id=settings.AWS_ACCOUNT_ID,
        )

    def upload_file(self, file_content: bytes, filename: str) -> None:
        try:
            self.s3.upload_fileobj(
                io.BytesIO(file_content), settings.AWS_BUCKET_NAME, filename
            )
            print(f"Upload complete: s3://{filename}")
        except Exception as e:
            print(f"Upload failed: {e}")
            raise e
