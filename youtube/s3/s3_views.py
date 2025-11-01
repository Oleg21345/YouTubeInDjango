from dotenv import load_dotenv
from io import BytesIO
import os
import boto3


load_dotenv()


class S3Client:
    def __init__(self, access_key: str, secret_key: str, bucket_name: str, region_name: str):

        self.bucket_name = bucket_name
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "region_name": region_name
        }

    def upload_files(self, file_obj, object_name=None):

        if object_name is None:
            object_name = getattr(file_obj, "name", "uploaded_file.webp")
        file_obj.seek(0)
        s3_client = boto3.client("s3", **self.config)

        s3_client.upload_fileobj(file_obj, self.bucket_name, object_name)

        return f"https://{self.bucket_name}.s3.{self.config['region_name']}.amazonaws.com/{object_name}"


def main(front_end_file):
    s3_client = S3Client(
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        bucket_name=os.getenv("AWS_STORAGE_BUCKET_NAME"),
        region_name=os.getenv("AWS_LOCATION")
    )
    return s3_client.upload_files(front_end_file)


def delete_s3_file(file_url):
    s3_client = boto3.client(
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_LOCATION")
    )
    bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")
    key = file_url.split(f"{bucket_name}/")[-1] if bucket_name in file_url else file_url.split(".com/")[-1]

    try:
        s3_client.delete_object(Bucket=bucket_name, Key=key)
        print(f"✅ Deleted from S3: {key}")
    except Exception as e:
        print(f"⚠️ Error deleting from S3: {e}")



