from datetime import datetime, timedelta, timezone
from config import *
import boto3

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
)

def create_presigned_upload_url(filename, content_type):
    bucket = S3_BUCKET
    key = f"uploads/{filename}"

    url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket, 
            "Key": key, 
            "ContentType": content_type},
        ExpiresIn=PRESIGNED_URL_EXPIRY
    )

    return {
        "url": url,
        "expires_at": (datetime.now(timezone.utc) + timedelta(seconds=PRESIGNED_URL_EXPIRY)).isoformat() + "Z",
        "key": key,
        "content_type": content_type
    }
