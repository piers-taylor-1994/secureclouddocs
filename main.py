from datetime import datetime, timezone
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def read_health():
    return {
        "status":"ok", 
        "time":datetime.now(timezone.utc).isoformat() + "Z"
    }