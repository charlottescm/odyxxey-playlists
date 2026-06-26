#!/usr/bin/env python3
"""
Odyxxey SoundCloud Playlist Scraper
Pulls track URLs from each playlist and saves to individual CSV files.
"""

import subprocess
import json
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


def get_track_urls(playlist_url: str, retries: int = 3) -> list[str]:
    """Use yt-dlp to extract all track URLs from a SoundCloud playlist."""
    for attempt in range(1, retries + 1):
        print(f"  Attempt {attempt}/{retries}...")
        result = subprocess.run(
            [
                "yt-dlp",
                "--no-flat-playlist",
                "--print", "webpage_url",
                "--no-warnings",
                "--extractor-args", "soundcloud:formats=0",
                playlist_url,
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode == 0:
            urls = [
                line.strip()
                for line in result.stdout.strip().split("\n")
                if line.strip() and "soundcloud.com" in line
            ]
            if urls:
                return urls

        print(f"  yt-dlp stderr: {result.stderr[:300]}")
        if attempt < retries:
            wait = attempt * 10
            print(f"  Retrying in {wait}s...")
            time.sleep(wait)

    return []


def save_csv(name: str, urls: list[str]):
    """Save track URLs to a CSV file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{name}.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["track_url"])
        for url in urls:
            writer.writerow([url])
    print(f"  Saved {len(urls)} tracks → {filepath}")


def main():
    print("=== Odyxxey SoundCloud Scraper ===\n")
    failed = []

    for name, url in PLAYLISTS.items():
        print(f"Scraping: {name}")
        urls = get_track_urls(url)
        if urls:
            save_csv(name, urls)
        else:
            print(f"  ERROR: No tracks found for {name}")
            failed.append(name)
        time.sleep(3)  # polite delay between playlists

    print("\n=== Done ===")
    if failed:
        print(f"Failed playlists: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("All playlists scraped successfully.")


if __name__ == "__main__":
    main()
