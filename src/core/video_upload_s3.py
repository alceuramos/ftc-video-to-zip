import boto3

from core.settings import settings


class S3StorageService:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            aws_account_id=settings.AWS_ACCOUNT_ID,
        )

    def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str,
    ):
        try:

            self.s3.put_object(
                Bucket=settings.AWS_BUCKET_NAME,
                Key=filename,
                Body=file_bytes,
                ContentType=content_type,
            )
        except Exception as e:
            raise ValueError(f"Failed to upload file to S3: {str(e)}")
