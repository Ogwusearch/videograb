from fastapi import APIRouter

from backend.app.schemas import VideoInfoRequest
from videograb.detector import detect_platform
from videograb.downloader import VideoDownloader

router = APIRouter(tags=["Video"])


@router.post("/info")
def get_video_info(request: VideoInfoRequest):
    url = str(request.url)

    downloader = VideoDownloader()
    info = downloader.get_info(url)

    return {
        "platform": detect_platform(url),
        "info": info,
    }