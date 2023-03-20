from uuid import uuid4

import boto3

from app.core.config import get_settings


class S3Service:
    settings = get_settings()

    @classmethod
    def upload_video(cls, video: bytes) -> str:
        file_key = str(uuid4())
        session = boto3.session.Session(aws_access_key_id=cls.settings.AWS_ACCESS_KEY,
                                        aws_secret_access_key=cls.settings.AWS_SECRET_ACCESS_KEY)
        s3 = session.resource('s3')
        s3.Bucket(cls.settings.AWS_S3_BUCKET_NAME).put_object(Key=file_key, Body=video)
        url = f"{cls.settings.aws_s3_bucket_file_url}{file_key}"
        return url

    @classmethod
    def delete_video(cls, file_url: str) -> None:
        session = boto3.session.Session(aws_access_key_id=cls.settings.AWS_ACCESS_KEY,
                                        aws_secret_access_key=cls.settings.AWS_SECRET_ACCESS_KEY)
        s3 = session.resource('s3')
        file_key = file_url.replace(cls.settings.aws_s3_bucket_file_url, "")
        s3.Object(cls.settings.AWS_S3_BUCKET_NAME, file_key).delete()
