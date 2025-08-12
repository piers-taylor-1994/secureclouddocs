from fastapi import HTTPException
from config import *

def validate_filename(filename):
    if not filename or not FILENAME_PATTERN.match(filename):
        raise HTTPException(status_code=400, detail="Invalid filename, only letters, dashes, underscores, dots and spaces allowed")

def validate_content_type(content_type):
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported content type.")