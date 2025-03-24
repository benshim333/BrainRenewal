# Automatically uploads videos to YouTube.

import os
import google.auth
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import google.oauth2.credentials
import google_auth_oauthlib.flow
import datetime as dt
import csv
import time

# OAuth2 authentication setup
client_secrets_file = "client_secret.json"
scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=credentials)

# Copied from generator.py
def sanitize_ref(ref):
    return ref.replace(" ", "_").replace(":", "_").replace("-", "_")

# Copied from generator.py
def csv_to_bible_passages(filename):
    passages = []
    
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Ensure the row is not empty
                book_chapter = row[0]  # First column contains "Book Chapter"
                for verse_range in row[1:]:  # Remaining columns contain verse ranges
                    if verse_range:
                        passages.append(f"{book_chapter}:{verse_range}")
    
    return passages

# Upload video to YouTube
def upload_video(youtube, title, publish_time, video_file):
    request = youtube.videos().insert(
        part="snippet,status",
        body= {"snippet": {
                "title": title,
                "description": "Thanks for watching this BrainRenewal Subway Surfers Bible video! Please subscribe and share with a friend to help renew the minds of Gen Z/Alpha.\n\n#shorts",
                "tags": ["bible", "religion", "scripture", "faith", "jesus", "god", "christianity", "christian", "apologetics", "brain", "rot", "shorts", "subway", "surfers"],
                "categoryId": 22,
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": publish_time
            }
        },
        media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
    )
    response = request.execute()
    print(f"Video for {title} successfully uploaded at youtube.com/watch?v={response["id"]}")

if __name__ == "__main__":
    youtube_service = get_authenticated_service()

    publish_time = dt.datetime(2025, 4, 11, 8, 7, 0, tzinfo=dt.timezone.utc) # Time that the first video should be uploaded (UTC)

    passages = csv_to_bible_passages("csv_files/Genesis.csv")[100:200]
    print(f"{len(passages)} passages found")

    for passage in passages:
        ref = sanitize_ref(passage)

        upload_video(youtube_service, passage, publish_time.isoformat(), f"video_files/{ref}.mp4")

        publish_time += dt.timedelta(hours=8) # Gap between videos