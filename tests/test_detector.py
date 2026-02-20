"""Tests for platform detection."""
import pytest
from videograb.detector import detect_platform, is_valid_url, is_playlist

@pytest.mark.parametrize("url,expected", [
    ("https://youtu.be/dQw4w9WgXcQ",                     "YouTube"),
    ("https://www.youtube.com/watch?v=abc",               "YouTube"),
    ("https://x.com/user/status/123",                     "X/Twitter"),
    ("https://twitter.com/user/status/456",               "X/Twitter"),
    ("https://www.instagram.com/reel/xyz/",               "Instagram"),
    ("https://www.snapchat.com/spotlight/abc",            "Snapchat"),
    ("https://www.tiktok.com/@user/video/123",            "TikTok"),
    ("https://www.facebook.com/watch?v=999",              "Facebook"),
    ("https://vimeo.com/123456",                          "Vimeo"),
    ("https://reddit.com/r/videos/comments/abc/title/",  "Reddit"),
    ("https://www.twitch.tv/videos/123456",               "Twitch"),
    ("https://some-random-site.com/video/clip.mp4",      "Website"),
])
def test_detect_platform(url, expected):
    assert detect_platform(url) == expected

def test_is_valid_url():
    assert is_valid_url("https://youtu.be/abc")  is True
    assert is_valid_url("http://example.com")    is True
    assert is_valid_url("not-a-url")             is False

def test_is_playlist():
    assert is_playlist("https://www.youtube.com/playlist?list=PLxyz") is True
    assert is_playlist("https://youtu.be/dQw4w9WgXcQ")                is False
