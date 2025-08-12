from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import boto3

load_dotenv()

s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION")
)

def created_presigned_upload_url(filename, content_type):
    bucket = os.getenv("S3_BUCKET")
    key = f"uploads/{filename}"

    url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket, 
            "Key": key, 
            "ContentType": content_type},
        ExpiresIn=300  # 5 minutes
    )

    return {
        "url": url,
        "expires_at": datetime.now(timezone.utc).isoformat() + "Z",
        "key": key,
        "content_type": content_type
    }