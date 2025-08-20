from config import AWS_REGION, S3_BUCKET, PRESIGNED_URL_EXPIRY
import boto3

def generate_presigned_upload_url(filename: str, content_type: str):
    key = f"uploads/{filename}"
    s3_client = boto3.client("s3", region_name=AWS_REGION)
    url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": S3_BUCKET, "Key": key, "ContentType": content_type},
        ExpiresIn=PRESIGNED_URL_EXPIRY
    )
    return url, key

