# BrainRenewal Docker Setup Guide

Follow these steps to get the Bible verse video generator running on your machine:

## 1. Install Docker Desktop
1. Download and install Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Start Docker Desktop and wait for it to fully initialize

## 2. Create Project Structure
1. Create a new directory for the project
2. Inside that directory, create these folders:
   - `audio_files` (for generated audio)
   - `video_files` (for generated videos)
   - `csv_files` (for your Bible verse CSV files)

## 3. Set Up YouTube API Access
1. Go to Google Cloud Console: https://console.cloud.google.com
2. Create a new project
3. Enable the YouTube Data API v3
4. Create OAuth 2.0 credentials
5. Download the credentials and save as `client_secret.json` in your project directory

## 4. Create docker-compose.yml
Create a file named `docker-compose.yml` with these contents:
```yaml
services:
  app:
    image: benshim333/brainrenewal:latest
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1
    ports:
      - "8080:8080"
```

## 5. Add Your Files
1. Place your Bible verse CSV files in the `csv_files` directory
2. Make sure `client_secret.json` is in the main project directory

## 6. Run the Container
Open a terminal in your project directory and run:
```bash
docker compose up -d
```

## 7. Using the Application
To generate videos:
```bash
docker compose exec app python3 generator.py
```

To upload videos to YouTube:
```bash
docker compose exec app python3 yt-uploader.py
```

## Troubleshooting
- If Docker isn't responding, try restarting Docker Desktop
- Make sure all required directories exist
- Verify that `client_secret.json` is present and valid
- Check that your CSV files are properly formatted

## File Structure
Your project directory should look like this:
```
your-project-directory/
├── docker-compose.yml
├── client_secret.json
├── audio_files/
├── video_files/
└── csv_files/
    └── your-bible-verses.csv
```
