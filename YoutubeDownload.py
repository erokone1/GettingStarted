from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import subprocess

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in " ._-" else "_" for c in name)

def download_video(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    print(f"Title: {yt.title}")

    # Sanitize the title to create a safe filename
    safe_title = sanitize_filename(yt.title)
    output_filename = f"{safe_title}.mp4"

    # Retrieve all video-only streams with mp4 extension
    video_streams = yt.streams.filter(adaptive=True, only_video=True, file_extension='mp4').order_by('resolution').desc()

    # Display available resolutions
    print("Available download options:")
    for idx, stream in enumerate(video_streams, start=1):
        print(f"{idx}. Resolution: {stream.resolution}, FPS: {stream.fps}, Type: {stream.mime_type}")

    # Prompt user to select a resolution
    while True:
        try:
            choice = int(input("Enter the number corresponding to your desired resolution: "))
            if 1 <= choice <= len(video_streams):
                video_stream = video_streams[choice - 1]
                break
            else:
                print("Invalid selection. Please choose a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Retrieve the highest quality audio-only stream
    audio_stream = yt.streams.filter(adaptive=True, only_audio=True, file_extension='mp4').order_by('abr').desc().first()
    if not audio_stream:
        print("No audio stream available.")
        return

    # Define temporary filenames
    video_filename = 'video_temp.mp4'
    audio_filename = 'audio_temp.mp4'

    # Download video and audio streams
    print("Downloading video...")
    video_stream.download(filename=video_filename)
    print("Downloading audio...")
    audio_stream.download(filename=audio_filename)

    # Merge video and audio using ffmpeg
    print("Merging video and audio...")
    subprocess.run([
        'ffmpeg', '-y',
        '-i', video_filename,
        '-i', audio_filename,
        '-c', 'copy',
        output_filename
    ])

    # Clean up temporary files
    os.remove(video_filename)
    os.remove(audio_filename)
    print(f"Download and merge complete: {output_filename}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_video(video_url)
