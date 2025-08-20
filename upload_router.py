from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from auth import get_current_user
from logging_config import logger
from config import *
from validators import *
from aws import generate_presigned_upload_url
from context import user_name_ctx

router = APIRouter(prefix="/files", tags=["uploads"])

class PresignUploadRequest(BaseModel):
    filename: str
    content_type: str
    metadata: Optional[dict] = None

class PresignUploadResponse(BaseModel):
    url: str
    expiry_timestamp: datetime
    key: str

@router.post(
    "/presign-upload",
    response_model=PresignUploadResponse,
    summary="Request presigned URL for direct upload"
)
def presign_upload(file: UploadFile = File(...), user: str = Depends(get_current_user)):
    user_name_ctx.set(user)
    filename = file.filename
    content_type = file.content_type

    validate_filename(filename)
    validate_content_type(content_type)

    presigned_url, key = generate_presigned_upload_url(filename, content_type)
    expiry_timestamp = (datetime.now(timezone.utc) + timedelta(PRESIGNED_URL_EXPIRY))

    logger.info(f"Presigned URL generated for {filename}", extra={"user_name": user})
    return {"url": presigned_url, "expiry_timestamp": expiry_timestamp, "key": key,}
