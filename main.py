from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, users_db
from logging_config import setup_logging, json, logger
from middleware import RequestIDMiddleware
from validators import *
from context import user_name_ctx
from upload_router import router
import traceback

#fastapi dev main.py

setup_logging()

app = FastAPI()
app.add_middleware(RequestIDMiddleware)
app.include_router(router)

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
def read_health():
    logger.info(f"Health check requested")
    return {
        "status":"ok", 
        "time":datetime.now(timezone.utc).isoformat() + "Z"
    }

@app.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or form_data.password != user["password"]:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user_name = user["username"], expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}