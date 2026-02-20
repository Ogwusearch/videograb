"""
Global configuration and constants.
"""

import os
from pathlib import Path

# Default output directory
DEFAULT_OUTPUT_DIR = Path.home() / "Downloads" / "VideoGrab"

# Quality presets
QUALITY_PRESETS = {
    "best":   "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "1080p":  "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
    "720p":   "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
    "480p":   "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]",
    "360p":   "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]",
    "worst":  "worstvideo+worstaudio/worst",
    "audio":  "bestaudio/best",
}

# Platform detection patterns
PLATFORM_PATTERNS = {
    "YouTube":      [r"(youtube\.com|youtu\.be)"],
    "X/Twitter":    [r"(twitter\.com|x\.com)"],
    "Instagram":    [r"instagram\.com"],
    "Snapchat":     [r"snapchat\.com"],
    "TikTok":       [r"tiktok\.com"],
    "Facebook":     [r"(facebook\.com|fb\.watch)"],
    "Vimeo":        [r"vimeo\.com"],
    "Reddit":       [r"(reddit\.com|redd\.it)"],
    "Dailymotion":  [r"dailymotion\.com"],
    "Twitch":       [r"twitch\.tv"],
    "Bilibili":     [r"bilibili\.com"],
    "Rumble":       [r"rumble\.com"],
    "Odysee":       [r"odysee\.com"],
}

# Platform-specific yt-dlp option overrides
PLATFORM_EXTRA_OPTS = {
    "X/Twitter": {
        "extractor_args": {"twitter": {"legacy_api": ["1"]}},
    },
    "YouTube": {},
    "Instagram": {},
    "Snapchat": {},
}

# Output filename template
OUTPUT_TEMPLATE = "%(uploader)s - %(title)s.%(ext)s"

# Retry settings
RETRIES               = 10
FRAGMENT_RETRIES      = 10
CONCURRENT_FRAGMENTS  = 4
