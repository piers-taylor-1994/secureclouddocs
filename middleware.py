from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from context import request_id_ctx, user_name_ctx
from logging_config import middleware_logger
from auth import get_current_user
import time

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid4())
        request_id_ctx.set(request_id)
        request.state.request_id = request_id

        try:
            current_user = await get_current_user(request)
            user_name_ctx.set(current_user or "")
        except Exception:
            user_name_ctx.set("")

        middleware_logger.info(f"request_start {request.method} {request.url}")

        start_time = time.perf_counter()

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        process_time = (time.perf_counter() - start_time) * 1000

        middleware_logger.info(
            f"request_end {request.method} {request.url} "
            f"status={response.status_code} duration={process_time:.2f}ms"
        )

        return response
