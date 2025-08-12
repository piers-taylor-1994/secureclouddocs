from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from logging_config import *

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID")
        if not request_id or not request_id.strip():
            request_id = str(uuid4())
        
        request.state.request_id = request_id
        request_id_ctx.set(request_id)
        
        response = await call_next(request)

        response.headers["X-Request-ID"] = request.state.request_id
        return response

