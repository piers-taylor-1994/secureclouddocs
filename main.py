from datetime import datetime, timezone
from fastapi import FastAPI, Body
from aws import create_presigned_upload_url
from logging_config import *
from validators import *
import logging

#fastapi dev main.py

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/health")
def read_health():
    return {
        "status":"ok", 
        "time":datetime.now(timezone.utc).isoformat() + "Z"
    }

@app.get("/generate-upload-url")
def generate_upload_url(filename):
    return create_presigned_upload_url(filename, "application/octet-stream")

@app.post("/upload")
def upload_file(filename: str = Body( ... ), content_type: str = Body( ... )):
    logger.info(f"Upload request for file: '{filename}' content type: '{content_type}'")
    validate_filename(filename)
    validate_content_type(content_type)

    return create_presigned_upload_url(filename, content_type)