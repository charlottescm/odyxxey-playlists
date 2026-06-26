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
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode == 0 or result.stdout.strip():
            clean_urls = []
            api_urls = []
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if not line or "soundcloud.com" not in line:
                    continue
                if line.startswith("https://api-v2"):
                    api_urls.append(line)
                else:
                    clean_urls.append(line)

            # Resolve any api-v2 URLs individually
            if api_urls:
                print(f"  Resolving {len(api_urls)} api-v2 URLs...")
                for api_url in api_urls:
                    resolved = resolve_api_url(api_url)
                    if resolved:
                        clean_urls.append(resolved)
                    else:
                        clean_urls.append(api_url)  # keep as fallback
                    time.sleep(1)

            if clean_urls:
                return clean_urls

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
    print(f"  Saved {len(urls)} tracks -> {filepath}")


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
        time.sleep(3)

    print("\n=== Done ===")
    if failed:
        print(f"Failed playlists: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("All playlists scraped successfully.")


if __name__ == "__main__":
    main()
