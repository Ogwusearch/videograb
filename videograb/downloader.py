"""
Core download engine wrapping yt-dlp.
"""

import re
from pathlib import Path
from typing import Optional, Callable

try:
    import yt_dlp
except ImportError:
    raise ImportError("yt-dlp is not installed. Run: pip install yt-dlp")

from videograb.config import (
    DEFAULT_OUTPUT_DIR, QUALITY_PRESETS, OUTPUT_TEMPLATE,
    PLATFORM_EXTRA_OPTS, RETRIES, FRAGMENT_RETRIES, CONCURRENT_FRAGMENTS,
)
from videograb.detector import detect_platform
from videograb.logger import get_logger

log = get_logger(__name__)


class VideoDownloader:
    """
    Universal video downloader.

    Parameters
    ----------
    output_dir     : Folder to save downloaded files
    quality        : One of the QUALITY_PRESETS keys or a raw yt-dlp format string
    audio_only     : Extract audio as MP3 instead of keeping video
    cookies_file   : Path to a Netscape cookies.txt for authenticated downloads
    cookies_browser: Browser name to pull cookies from (e.g. 'chrome', 'firefox')
    proxy          : Proxy URL (e.g. socks5://127.0.0.1:1080)
    subtitles      : Download subtitles alongside the video
    verbose        : Pass yt-dlp verbose output to stdout
    on_progress    : Optional callback(d) called on each yt-dlp progress hook event
    """

    def __init__(
        self,
        output_dir: str | Path = DEFAULT_OUTPUT_DIR,
        quality: str = "best",
        audio_only: bool = False,
        cookies_file: Optional[str] = None,
        cookies_browser: Optional[str] = None,
        proxy: Optional[str] = None,
        subtitles: bool = False,
        verbose: bool = False,
        on_progress: Optional[Callable] = None,
    ):
        self.output_dir      = Path(output_dir)
        self.quality         = quality
        self.audio_only      = audio_only
        self.cookies_file    = cookies_file
        self.cookies_browser = cookies_browser
        self.proxy           = proxy
        self.subtitles       = subtitles
        self.verbose         = verbose
        self.on_progress     = on_progress

        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── Private helpers ──────────────────────────────────────

    def _format_string(self) -> str:
        if self.audio_only:
            return QUALITY_PRESETS["audio"]
        return QUALITY_PRESETS.get(self.quality, self.quality)

    def _build_opts(self, platform: str) -> dict:
        outtmpl = str(self.output_dir / OUTPUT_TEMPLATE)

        opts: dict = {
            "format":                      self._format_string(),
            "outtmpl":                     outtmpl,
            "quiet":                       not self.verbose,
            "no_warnings":                 not self.verbose,
            "merge_output_format":         "mp4",
            "retries":                     RETRIES,
            "fragment_retries":            FRAGMENT_RETRIES,
            "concurrent_fragment_downloads": CONCURRENT_FRAGMENTS,
            "progress_hooks":              [self._hook],
            "postprocessors":              [],
            "writesubtitles":              self.subtitles,
            "subtitleslangs":              ["en"] if self.subtitles else [],
        }

        if self.audio_only:
            opts["postprocessors"].append({
                "key":              "FFmpegExtractAudio",
                "preferredcodec":   "mp3",
                "preferredquality": "192",
            })

        if self.cookies_file:
            opts["cookiefile"] = self.cookies_file

        if self.cookies_browser:
            opts["cookiesfrombrowser"] = (self.cookies_browser,)

        if self.proxy:
            opts["proxy"] = self.proxy

        # Merge platform-specific overrides
        opts.update(PLATFORM_EXTRA_OPTS.get(platform, {}))

        return opts

    def _hook(self, d: dict):
        if self.on_progress:
            self.on_progress(d)

    # ── Public API ───────────────────────────────────────────

    def get_info(self, url: str) -> dict:
        """Return video metadata dict without downloading."""
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
            try:
                return ydl.extract_info(url, download=False)
            except Exception as exc:
                log.error("Info extraction failed: %s", exc)
                return {"error": str(exc)}

    def download(self, url: str) -> bool:
        """Download a single URL. Returns True on success."""
        platform = detect_platform(url)
        log.info("Platform: %s | URL: %s", platform, url)
        opts = self._build_opts(platform)
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            return True
        except yt_dlp.utils.DownloadError as exc:
            log.error("Download error: %s", exc)
            return False
        except Exception as exc:
            log.error("Unexpected error: %s", exc)
            return False

    def batch_download(self, urls: list[str]) -> dict:
        """Download a list of URLs. Returns success/failed lists."""
        results = {"success": [], "failed": []}
        total = len(urls)
        for idx, url in enumerate(urls, 1):
            url = url.strip()
            if not url or url.startswith("#"):
                continue
            log.info("(%d/%d) %s", idx, total, url)
            if self.download(url):
                results["success"].append(url)
            else:
                results["failed"].append(url)
        return results
