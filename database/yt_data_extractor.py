"""
YouTube Data Extractor Module

This module provides a class for extracting metadata and audio from YouTube videos using the
`pytubefix` and `pydub` libraries. It includes methods to retrieve the video's length, title,
publish date, and to download and convert its audio to MP3 format.

Dependencies:
- pytubefix
- pydub
- ffmpeg (must be installed and accessible via system path for audio conversion)

Classes:
    YouTubeDataExtractor
"""
import os

from pydub import AudioSegment
from pytubefix import YouTube
from pytubefix.cli import on_progress

class YouTubeDataExtractor:
    """
    A class to extract various types of data and audio from a YouTube video.
    """

    def __init__(self):
        """
        Initializes the YouTubeDataExtractor instance.
        """
        pass

    def extract_length_from_youtube_video(self, youtube_url):
        """
        Extracts the duration (in seconds) of a YouTube video.

        Args:
            youtube_url (str): URL of the YouTube video.

        Returns:
            int: Length of the video in seconds.
        """
        yt = YouTube(youtube_url, on_progress_callback=on_progress)
        return yt.length

    def extract_title_from_youtube_video(self, youtube_url):
        """
        Extracts the title of a YouTube video.

        Args:
            youtube_url (str): URL of the YouTube video.

        Returns:
            str: Title of the video.
        """
        yt = YouTube(youtube_url, on_progress_callback=on_progress)
        return yt.title

    def extract_publish_date_from_youtube_video(self, youtube_url):
        """
        Extracts the publish date of a YouTube video, if available.

        Args:
            youtube_url (str): URL of the YouTube video.

        Returns:
            str or None: Publish date in string format, or None if not found.
        """
        yt = YouTube(youtube_url, on_progress_callback=on_progress)
        details = yt.vid_details

        keys_path = [
            "engagementPanels", "2", "engagementPanelSectionListRenderer", "content",
            "structuredDescriptionContentRenderer", "items", "0",
            "videoDescriptionHeaderRenderer", "publishDate", "simpleText"
        ]

        try:
            for key in keys_path:
                if isinstance(details, list):
                    key = int(key)
                details = details[key]
            return details
        except (KeyError, IndexError, TypeError, ValueError):
            return None

    def extract_audio_from_youtube_video(self, youtube_url: str, output_path: str):
        """
        Downloads the audio track from a YouTube video and converts it to MP3 format.

        Args:
            youtube_url (str): URL of the YouTube video.
            output_path (str): Directory where the MP3 file will be saved.

        Returns:
            str: Full path to the saved MP3 audio file.
        """
        yt_title = self.extract_title_from_youtube_video(youtube_url)
        yt = YouTube(
            youtube_url,
            on_progress_callback=on_progress,
            use_oauth=True,
            client='MWEB',
            allow_oauth_cache=True
        )
        ys = yt.streams.get_audio_only()

        filename = f'{yt_title}'
        audio_path = ys.download(output_path=output_path, filename=filename)

        mp3_path = os.path.splitext(audio_path)[0] + ".mp3"
        audio = AudioSegment.from_file(audio_path)
        audio.export(mp3_path, format="mp3")

        os.remove(audio_path)

        return mp3_path
