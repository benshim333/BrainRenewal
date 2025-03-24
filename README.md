# BrainRenewal

A project that generates and uploads Bible verse videos to YouTube.

## Prerequisites

- Docker Desktop installed on your machine
- A `client_secret.json` file from Google Cloud Console for YouTube API access
- Input CSV files in the `csv_files` directory

## Quick Start

1. Clone this repository
2. Place your `client_secret.json` in the root directory
3. Put your CSV files in the `csv_files` directory
4. Run the container:
```bash
docker compose up --build
```

5. To generate videos:
```bash
docker compose exec app python3 generator.py
```

6. To upload videos:
```bash
docker compose exec app python3 yt-uploader.py
```

## Directory Structure

- `audio_files/` - Generated audio files
- `video_files/` - Generated video files
- `csv_files/` - Input CSV files with Bible passages
- `client_secret.json` - YouTube API credentials

## Note

The container is configured to ignore mp3 and mp4 files during build for efficiency. These files are accessed through volume mounting when running the container.
