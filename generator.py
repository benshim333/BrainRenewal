# Given a CSV file with Bible passages, generates one video for each passage.

import sys
import os
import requests
import pyttsx3
import moviepy
import csv

# Fetch Bible verses.
def get_bible_verses(passage):
    response = requests.get(f"https://bible-api.com/{passage}")
    data = response.json()
    verses = data["text"]
    return verses

# Replace all occurrences of spaces, colons, and hyphens with underscores.
def sanitize_ref(ref):
    return ref.replace(" ", "_").replace(":", "_").replace("-", "_")

# Reads a CSV file and returns a list of Bible passages.
def csv_to_bible_passages(filename):
    """
    Each row of the CSV file should have the following format:
    Book Chapter,Verse Range,Verse Range,Verse Range,Verse Range,Verse Range
    For example:
    Genesis 1,1-5,6-8,9-13,14-19,20-23,24-26,27-31
    Genesis 2,1-3,4-6,7-9,10-14,15-17,18-20,21-25
    Genesis 3,1-5,6-8,9-13,14-16,17-19,20-24,
    """
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

if __name__ == "__main__":

    engine = pyttsx3.init() # Initialize text-to-speech engine
    engine.setProperty("rate", 150)
    passages = csv_to_bible_passages("csv_files/Exodus.csv")
    print(f"{len(passages)} passages found")
    cumulative_length = 0 # Start time for clip extraction

    sys.stdout = open(os.devnull, "w") # Suppress output
    sys.stderr = open(os.devnull, "w")
    video_clip = moviepy.VideoFileClip("video.mp4")
    sys.stdout = sys.__stdout__ # Restore output
    sys.stderr = sys.__stderr__

    for passage in passages:

        verses = get_bible_verses(passage)
        ref = sanitize_ref(passage)
        engine.save_to_file(verses, f"audio_files/{ref}.mp3")
        engine.runAndWait()
        audio_clip = moviepy.AudioFileClip(f"audio_files/{ref}.mp3")
        sub_clip = video_clip.subclipped(cumulative_length, cumulative_length + audio_clip.duration)
        cropped_clip = sub_clip.cropped(x1=710, y1=0, x2=1210, y2=1080) # Crop out the black bars on the sides
        resized_clip = cropped_clip.resized(height=1920, width=1080) # Dimensions of final video
        final_clip = resized_clip.with_audio(audio_clip)
        final_clip.write_videofile(f"video_files/{ref}.mp4", logger=None)
        cumulative_length += audio_clip.duration # Keep track of position in video

        print(f"{passage} completed; passage length {audio_clip.duration} seconds; cumulative length {round(cumulative_length, 2)} seconds")