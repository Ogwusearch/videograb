from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

from backend.app.schemas import DownloadRequest
from backend.app.services.video_service import VideoService

router = APIRouter(tags=["Downloads"])

service = VideoService()


def iter_file(
    file_path: Path,
    chunk_size: int = 1024 * 1024,
):
    """
    Stream the file in 1 MB chunks.
    """
    with file_path.open("rb") as file:
        while chunk := file.read(chunk_size):
            yield chunk


def cleanup_temp_directory(temp_dir: Path) -> None:
    """
    Delete the temporary download directory after
    the response has finished streaming.
    """
    shutil.rmtree(
        temp_dir,
        ignore_errors=True,
    )


@router.post("/download")
def download_video(request: DownloadRequest):
    try:
        temp_dir, file_path = service.download(
            url=str(request.url),
            quality=request.quality,
            audio_only=request.audio_only,
        )

        return StreamingResponse(
            iter_file(file_path),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": (
                    f'attachment; filename="{file_path.name}"'
                )
            },
            background=BackgroundTask(
                cleanup_temp_directory,
                temp_dir,
            ),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc