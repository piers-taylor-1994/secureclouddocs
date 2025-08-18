import logging
import json
from config import LOG_LEVEL
from context import request_id_ctx, user_name_ctx

class RequestIDFilter(logging.Filter):
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

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler.addFilter(RequestIDFilter())

    logger = logging.getLogger("securecloud")
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(handler)