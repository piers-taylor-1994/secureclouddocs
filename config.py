from dotenv import load_dotenv
import os

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")  # sensible default
S3_BUCKET = os.getenv("S3_BUCKET")
PRESIGNED_URL_EXPIRY = int(os.getenv("PRESIGNED_URL_EXPIRY", "300"))
ALLOWED_CONTENT_TYPES = {
    "application/json",
    "image/jpeg",
    "image/png",
    "application/pdf",
    "application/octet-stream",
}
MAX_FILENAME_LENGTH = int(os.getenv("MAX_FILENAME_LENGTH", "128"))

if not S3_BUCKET:
    raise RuntimeError("S3_BUCKET is not set in environment variables.")
