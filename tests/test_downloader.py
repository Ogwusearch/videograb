"""Tests for VideoDownloader (mocked yt-dlp)."""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from videograb.downloader import VideoDownloader

@pytest.fixture
def downloader(tmp_path):
    return VideoDownloader(output_dir=tmp_path)

def test_output_dir_created(tmp_path):
    new_dir = tmp_path / "new_subdir"
    dl = VideoDownloader(output_dir=new_dir)
    assert new_dir.exists()

def test_format_string_best(downloader):
    assert "bestvideo" in downloader._format_string()

def test_format_string_audio_only(tmp_path):
    dl = VideoDownloader(output_dir=tmp_path, audio_only=True)
    assert "bestaudio" in dl._format_string()

def test_format_string_720p(tmp_path):
    dl = VideoDownloader(output_dir=tmp_path, quality="720p")
    assert "720" in dl._format_string()

@patch("videograb.downloader.yt_dlp.YoutubeDL")
def test_download_success(mock_ydl_cls, downloader):
    mock_ydl = MagicMock()
    mock_ydl_cls.return_value.__enter__.return_value = mock_ydl
    result = downloader.download("https://youtu.be/dQw4w9WgXcQ")
    assert result is True
    mock_ydl.download.assert_called_once()

@patch("videograb.downloader.yt_dlp.YoutubeDL")
def test_download_failure(mock_ydl_cls, downloader):
    import yt_dlp
    mock_ydl = MagicMock()
    mock_ydl.download.side_effect = yt_dlp.utils.DownloadError("fail")
    mock_ydl_cls.return_value.__enter__.return_value = mock_ydl
    result = downloader.download("https://youtu.be/bad")
    assert result is False

@patch("videograb.downloader.yt_dlp.YoutubeDL")
def test_batch_download(mock_ydl_cls, downloader):
    mock_ydl = MagicMock()
    mock_ydl_cls.return_value.__enter__.return_value = mock_ydl
    urls = [
        "https://youtu.be/aaa",
        "# This is a comment",
        "",
        "https://youtu.be/bbb",
    ]
    results = downloader.batch_download(urls)
    assert len(results["success"]) == 2
    assert len(results["failed"])  == 0
