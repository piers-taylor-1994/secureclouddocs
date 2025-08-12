from datetime import datetime, timezone
from fastapi import FastAPI, Body, HTTPException
from aws import created_presigned_upload_url
from validators import *

app = FastAPI()

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
    validate_filename(filename)
    validate_content_type(content_type)
    
    return created_presigned_upload_url(filename, content_type)