from pydantic import BaseModel, HttpUrl


class VideoInfoRequest(BaseModel):
    url: HttpUrl


class DownloadRequest(BaseModel):
    url: HttpUrl
    quality: str = "best"
    audio_only: bool = False