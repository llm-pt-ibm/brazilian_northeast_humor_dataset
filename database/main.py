import pandas as pd

from database_creation.yt_data_extractor import *
from yt_video_transcriber import *

def extract_audios_from_youtube_videos():
    yt_data_extractor = YouTubeDataExtractor()
    yt_videos = pd.read_csv('data/videos/youtube_videos.csv')
    for video_url in yt_videos['video_url']:
        try:
            yt_data_extractor.extract_audio_from_youtube_video(video_url, 'data/audios')
            print('Step completed.')
        except Exception as e:
            print(e)
            print(f'Step failed for url {video_url}.')

extract_audios_from_youtube_videos()

def extract_transcripts_from_youtube_videos():
    yt_transcriber = YouTubeVideoTranscriber()
    yt_transcriber.transcribe_youtube_videos()

extract_transcripts_from_youtube_videos()