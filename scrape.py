#!/usr/bin/env python3
"""
Odyxxey SoundCloud Playlist Scraper
Pulls track URLs from each playlist and saves to individual CSV files.
"""

import subprocess
import csv
import os
import sys
import time

PLAYLISTS = {
    "odyxxey-radio-2020": "https://soundcloud.com/odyxxey/sets/odyxxey-radio-2020",
    "odyxxey-radio-2021": "https://soundcloud.com/odyxxey/sets/odyxxey-radio-2021",
    "odyxxey-radio-2022": "https://soundcloud.com/odyxxey/sets/odyxxey-radio-2022",
    "odyxxey-radio-2023": "https://soundcloud.com/odyxxey/sets/odyxxey-radio-2023",
    "odyxxey-radio-2024": "https://soundcloud.com/odyxxey/sets/odyxxey-radio-2024",
    "odyxxey-radio-2025": "https://soundcloud.com/odyxxey/sets/odyxxey-radio-2025",
    "odyxxey-radio-2026": "https://soundcloud.com/odyxxey/sets/odyxxey-radio-2026",
}

OUTPUT_DIR = "data"


def resolve_api_url(api_url: str) -> str | None:
    """Resolve an api-v2.soundcloud.com/tracks/{id} URL to a proper permalink."""
    result = subprocess.run(
        [
            "yt-dlp",
            "--flat-playlist",
            "--print", "webpage_url",
            "--no-warnings",
            api_url,
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line and "soundcloud.com" in line and not line.startswith("https://api-v2"):
            return line
    return None


def get_track_urls(playlist_url: str, retries: int = 3) -> list[str]:
    """Use yt-dlp to extract all track URLs from a SoundCloud playlist."""
    for attempt in range(1, retries + 1):
        print(f"  Attempt {attempt}/{retries}...")
        result = subprocess.run(
            [
                "yt-dlp",
                "--flat-playlist",
                "--print", "webpage_url",
                "--no-warnings",
                playlist_url,
            ],
