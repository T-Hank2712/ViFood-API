from uuid import uuid4

import boto3
from botocore.config import Config


class S3Service:
    ALLOWED_CONTENT_TYPES = {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/webp": "webp",
    }

    def __init__(self, settings):
        self.bucket = settings.aws_s3_bucket
        self.client = boto3.client(
            "s3",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            config=Config(signature_version="s3v4"),
        )

    def upload_file(
        self,
        user_id: str,
        file_content: bytes,
        content_type: str,
    ) -> str:
        extension = self._get_extension(content_type)
        s3_key = self._build_scan_key(user_id, extension)

        self.client.put_object(
            Bucket=self.bucket,
            Key=s3_key,
            Body=file_content,
            ContentType=content_type,
        )

        return s3_key

    def create_upload_url(self, user_id: str, content_type: str) -> dict:
        extension = self._get_extension(content_type)
        s3_key = self._build_scan_key(user_id, extension)

        upload_url = self.client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": self.bucket,
                "Key": s3_key,
                "ContentType": content_type,
            },
            ExpiresIn=300,
        )

        return {
            "upload_url": upload_url,
            "s3_key": s3_key,
        }

    def create_download_url(self, s3_key: str) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket,
                "Key": s3_key,
            },
            ExpiresIn=300,
        )

    def _build_scan_key(self, user_id: str, extension: str) -> str:
        return f"users/{user_id}/scans/{uuid4()}.{extension}"

    def _get_extension(self, content_type: str) -> str:
        if content_type not in self.ALLOWED_CONTENT_TYPES:
            raise ValueError(f"Unsupported content type: {content_type}")

        return self.ALLOWED_CONTENT_TYPES[content_type]
