from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.health import router as health_router
from backend.app.routes.info import router as info_router
from backend.app.routes.download import router as download_router

app = FastAPI(
    title="VideoGrab API",
    description="Web API for VideoGrab",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(info_router, prefix="/api")
app.include_router(download_router, prefix="/api")


@app.get("/")
def root():
    return {
        "name": "VideoGrab API",
        "version": "1.0.0",
        "status": "online",
    }