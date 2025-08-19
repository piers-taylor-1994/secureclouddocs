import logging
import json
from config import LOG_LEVEL
from context import request_id_ctx, user_name_ctx

class RequestContextFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_ctx.get() or ""
        record.user_name = user_name_ctx.get() or ""
        return True

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": record.request_id,
            "user_name": record.user_name
        }
        return json.dumps(log_obj)

logger = logging.getLogger("securecloud")
middleware_logger = logging.getLogger("securecloud.middleware")
middleware_logger.setLevel(logging.WARNING)  # hide normal request_start/end by default

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler.addFilter(RequestContextFilter())

    # Root logger (so plain logging.info() works too)
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    root_logger.addHandler(handler)

    # Named logger
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(handler)
    logger.propagate = False