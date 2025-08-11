from datetime import datetime, timezone
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import boto3

load_dotenv()

app = FastAPI()
s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION")
)

@app.get("/health")
def read_health():
    return {
        "status":"ok", 
        "time":datetime.now(timezone.utc).isoformat() + "Z"
    }

@app.get("/generate-upload-url")
def generate_upload_url(filename):
    bucket = os.getenv("S3_BUCKET")
    key = f"uploads/{filename}"
    url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=300  # 5 minutes
    )
    return {
        "url": url,
        "expires_at": datetime.now(timezone.utc).isoformat() + "Z",
        "key": key
    }