from datetime import datetime, timezone
from fastapi import FastAPI, Body, Request
from fastapi.responses import JSONResponse
from aws import create_presigned_upload_url
from logging_config import setup_logging, json
from middleware import RequestIDMiddleware
from validators import *

import logging
import traceback

#fastapi dev main.py

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(RequestIDMiddleware)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        json.dumps({
            "error": str(exc),
            "path": request.url.path,
            "method": request.method,
            "trace": traceback.format_exc(),
            "request_id": request.state.request_id
        }),
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.get("/health")
def read_health(request: Request):
    logger.info(f"Health check requested", extra={"request_id": request.state.request_id})
    return {
        "status":"ok", 
        "time":datetime.now(timezone.utc).isoformat() + "Z"
    }

@app.get("/generate-upload-url")
def generate_upload_url(request:Request, filename):
    logger.info(f"Presigned upload url requested for file '{filename}'", extra={"request_id": request.state.request_id})
    return create_presigned_upload_url(filename, "application/octet-stream")

@app.post("/upload")
def upload_file(request: Request, filename: str = Body( ... ), content_type: str = Body( ... )):
    logger.info(f"Upload request for file: '{filename}' content type: '{content_type}'", extra={"request_id": request.state.request_id})
    validate_filename(filename)
    validate_content_type(content_type)

    return create_presigned_upload_url(filename, content_type)