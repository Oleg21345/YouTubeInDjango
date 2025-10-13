from contextlib import contextmanager
from botocore.session import get_session
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
load_dotenv()

class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()


    @contextmanager
    def get_client(self):
        client = self.session.create_client("s3", **self.config)
        yield client

    def upload_file(
            self,
            file_obj
    ):
        object_name = getattr(file_obj, "name", "uploaded_file.webp")

        with self.get_client() as client:
            client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_obj.read()
            )
        return f"{self.config['endpoint_url']}/{self.bucket_name}/{object_name}"


def main(front_end_file):
    s3_client = S3Client(
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
        bucket_name=os.getenv("AWS_STORAGE_BUCKET_NAME")
    )
    return s3_client.upload_file(front_end_file)



