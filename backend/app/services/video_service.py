from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from videograb.downloader import VideoDownloader


class VideoService:
    def download(
        self,
        url: str,
        quality: str = "best",
        audio_only: bool = False,
    ) -> tuple[Path, Path]:
        """
        Download media into a temporary directory.

        Returns:
            tuple[Path, Path]:
                (temporary_directory, downloaded_file)

        The caller is responsible for cleaning up the temporary directory
        after the file has been streamed to the browser.
        """

        temp_dir = Path(
            tempfile.mkdtemp(prefix="videograb-")
        )

        try:
            downloader = VideoDownloader(
                output_dir=temp_dir,
                quality=quality,
                audio_only=audio_only,
            )

            success = downloader.download(url)

            if not success:
                raise RuntimeError("Download failed")

            files = [
                file
                for file in temp_dir.iterdir()
                if file.is_file()
            ]

            if not files:
                raise RuntimeError(
                    "Download completed but no file was produced"
                )

            # If multiple files exist, use the largest file as
            # the resulting media file.
            output_file = max(
                files,
                key=lambda file: file.stat().st_size,
            )

            return temp_dir, output_file

        except Exception:
            # Clean up immediately when the download itself fails.
            shutil.rmtree(
                temp_dir,
                ignore_errors=True,
            )
            raise