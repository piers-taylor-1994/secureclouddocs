from fastapi import HTTPException, status
from datetime import datetime, timezone
from context import request_id_ctx, user_name_ctx

def validate_presigned_url(params: dict):
    """
    Validates presigned URL parameters.
    Expected keys: 'expires_in', 'method', 'filename'
    """
    errors = []

    # Expiry check
    expires_in = params.get("expires_in")
    if not expires_in or int(expires_in) < int(datetime.now(timezone.utc).timestamp()):
        errors.append("URL has expired")

    # Method restriction
    method = (params.get("method") or "").upper()
    if method not in ["GET", "PUT"]:
        errors.append(f"Invalid method: {method}")

    # Filename validation
    filename = (params.get("filename") or "")
    if ".." in filename or filename.startswith("/"):
        errors.append("Invalid filename format")

    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors}
        )
