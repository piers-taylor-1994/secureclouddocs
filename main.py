from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Body, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, users_db
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

@app.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or form_data.password != user["password"]:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user_name = user["username"], expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/secure/presigned-url")
def secure_endpoint(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}. Here's your presigned URL placeholder."}