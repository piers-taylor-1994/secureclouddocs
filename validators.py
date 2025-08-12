from fastapi import HTTPException
from config import *

def validate_filename(filename):
    if not filename:
        raise HTTPException(status_code=400, detail="Invalid filename, cannot be blank.")

def validate_content_type(content_type):
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported content type.")