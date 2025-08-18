from contextvars import ContextVar

request_id_ctx = ContextVar("request_id", default="")
user_name_ctx = ContextVar("user_name", default="")