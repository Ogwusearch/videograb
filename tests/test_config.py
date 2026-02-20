"""Tests for config integrity."""
from videograb.config import QUALITY_PRESETS, PLATFORM_PATTERNS

def test_quality_presets_keys():
    required = {"best", "1080p", "720p", "480p", "360p", "worst", "audio"}
    assert required.issubset(QUALITY_PRESETS.keys())

def test_platform_patterns_not_empty():
    for platform, patterns in PLATFORM_PATTERNS.items():
        assert len(patterns) > 0, f"{platform} has no patterns"
