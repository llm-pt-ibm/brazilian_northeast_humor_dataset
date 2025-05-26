"""
YouTube Video Transcriber Module

This module defines a class to automate the process of:
1. Extracting metadata from YouTube videos,
2. Downloading and converting audio to MP3,
3. Transcribing the audio using a speech-to-text model (e.g., Whisper),
4. Storing all extracted information in a CSV file.

Dependencies:
- pandas
- os
- yt_data_extractor (local module with the YouTubeDataExtractor class)
- whisper_audio_transcriber (local module with the WhisperAudioTranscriber class)

Class:
    YouTubeVideoTranscriber
"""
import pandas as pd
import os

from yt_data_extractor import *
from whisper_audio_transcriber import *


class YouTubeVideoTranscriber:
    """
    A class to handle the transcription pipeline for YouTube videos, including
    metadata extraction, audio download, transcription, and CSV export.
    """

    def __init__(self):
        """
        Initializes default paths for audio, transcription, and video data directories.
        """
        self.audios_path = os.path.join(os.getcwd(), 'data', 'audios')
        self.transcriptions_path = os.path.join(os.getcwd(), 'data', 'transcriptions')
        self.videos_path = os.path.join(os.getcwd(), 'data', 'videos')

    def transcribe_youtube_videos(self):
        """
        Executes the complete pipeline:
        - Reads a list of YouTube video URLs from a CSV file ('youtube_videos.csv')
        - Extracts video title, duration, and publish date
        - Downloads and converts audio to MP3 format
        - Transcribes the audio using Whisper
        - Appends metadata and transcription to a CSV file

        If a transcription CSV already exists, processing resumes from the last completed row.
        """
        if not os.path.exists(self.transcriptions_path):
            os.makedirs(self.transcriptions_path)

        # Initialize or load existing CSV
        start_index = 0
        new_df = pd.DataFrame(columns=[
            'video_url', 'brazilian_state', 'video_title',
            'video_length_seconds', 'publish_date',
            'transcription', 'audio_path'
        ])
        new_csv_path = os.path.join(self.transcriptions_path, 'youtube_videos_transcribed_with_metadata.csv')

        if os.path.exists(new_csv_path):
            new_df = pd.read_csv(new_csv_path)
            start_index = len(new_df)

        data_extractor = YouTubeDataExtractor()
        whisper_model = WhisperAudioTranscriber()

        # Load video list
        df = pd.read_csv(os.path.join(self.videos_path, 'youtube_videos.csv'))

        for i, infos in df.iloc[start_index:].iterrows():
            url = infos['video_url']
            brazilian_state = infos['brazilian_state']

            try:
                video_title = data_extractor.extract_title_from_youtube_video(url)
            except:
                video_title = ''

            try:
                video_length = data_extractor.extract_length_from_youtube_video(url)
            except:
                video_length = ''

            try:
                publish_date = data_extractor.extract_publish_date_from_youtube_video(url)
            except:
                publish_date = ''

            try:
                audio_path = data_extractor.extract_audio_from_youtube_video(url, self.audios_path)
            except:
                audio_path = ''

            if audio_path:
                transcription = whisper_model.extract_text_from_audio(audio_path)
            else:
                transcription = ''

            new_row = {
                'video_url': url,
                'brazilian_state': brazilian_state,
                'video_title': video_title,
                'video_length_seconds': video_length,
                'publish_date': publish_date,
                'transcription': transcription,
                'audio_path': audio_path
            }

            new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)
            new_df.to_csv(new_csv_path, index=False)
