from datetime import datetime, timezone
from fastapi import FastAPI, Body
from dotenv import load_dotenv
import os
import boto3

load_dotenv()

app = FastAPI()
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

@app.get("/health")
def read_health():
    return {
        "status":"ok", 
        "time":datetime.now(timezone.utc).isoformat() + "Z"
    }

@app.get("/generate-upload-url")
def generate_upload_url(filename):
    return created_presigned_upload_url(filename, "application/octet-stream")

@app.post("/upload")
def upload_file(filename: str = Body( ... ), content_type: str = Body( ... )):
    return created_presigned_upload_url(filename, content_type)