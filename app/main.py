import os
import socket
import time

from fastapi import FastAPI

app = FastAPI(
    title="DevOps Lab API",
    version=os.getenv("APP_VERSION", "dev"),
)

started_at = time.time()


@app.get("/")
def root():
    return {
        "service": "devops-lab-api",
        "message": "Hello from Kubernetes",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.get("/version")
def version():
    return {
        "version": os.getenv("APP_VERSION", "dev"),
        "hostname": socket.gethostname(),
        "uptime_seconds": round(time.time() - started_at, 2),
    }
