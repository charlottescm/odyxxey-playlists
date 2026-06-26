# Odyxxey SoundCloud Playlist Scraper

Automatically pulls track URLs from Odyxxey Radio playlists into CSV files.
Runs every Wednesday at 06:00 UTC via GitHub Actions.

## Output

One CSV per playlist in the `data/` folder:

```
data/
  odyxxey-radio-2020.csv
  odyxxey-radio-2021.csv
  odyxxey-radio-2022.csv
  odyxxey-radio-2023.csv
  odyxxey-radio-2024.csv
  odyxxey-radio-2025.csv
  odyxxey-radio-2026.csv
```

Each file has a single column: `track_url`

## Setup (one time)

### 1. Create a GitHub repository

- Go to [github.com/new](https://github.com/new)
- Name it e.g. `odyxxey-playlists`
- Set to **Private** if you prefer
- Click **Create repository**

### 2. Upload these files

Either use the GitHub web UI (drag and drop) or via terminal:

```bash
git init
git add .
git commit -m "init"
git remote add origin https://github.com/YOUR_USERNAME/odyxxey-playlists.git
git push -u origin main
```

### 3. Enable Actions write permissions

Go to your repo → **Settings** → **Actions** → **General** → scroll to
**Workflow permissions** → select **Read and write permissions** → Save.

That's it. The scraper runs automatically every Wednesday.

## Manual run

Go to **Actions** tab in your repo → click **Scrape Odyxxey Playlists** →
click **Run workflow** → **Run workflow**.

## Adding or changing playlists

Edit the `PLAYLISTS` dictionary in `scrape.py`.
