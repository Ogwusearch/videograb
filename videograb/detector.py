"""
Platform detection from URL.
"""

import re
from videograb.config import PLATFORM_PATTERNS


def detect_platform(url: str) -> str:
    """Return the platform name for a given URL."""
    for platform, patterns in PLATFORM_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return platform
    return "Website"


def is_playlist(url: str) -> bool:
    """Heuristic check for playlist URLs."""
    indicators = ["playlist?list=", "/playlist/", "/sets/", "/collection/"]
    return any(ind in url.lower() for ind in indicators)


def is_valid_url(url: str) -> bool:
    """Basic URL validation."""
    return url.startswith(("http://", "https://"))
