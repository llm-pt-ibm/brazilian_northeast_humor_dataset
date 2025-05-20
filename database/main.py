import pandas as pd

from yt_data_extractor import *
from yt_video_transcriber import *

def extract_audios_from_youtube_videos():
    yt_data_extractor = YouTubeDataExtractor()
    yt_videos = pd.read_csv('data/videos/youtube_videos.csv')
    for video_url in yt_videos['video_url']:
        try:
            yt_data_extractor.extract_audio_from_youtube_video(video_url, 'data/audios')
            print('Step completed.')
        except Exception as e:
            print(f'Step failed for url {video_url}.\n{e}')

def extract_transcripts_from_youtube_videos():
    yt_transcriber = YouTubeVideoTranscriber()
    yt_transcriber.transcribe_youtube_videos()

def organize_final_dataset():
    annotated_df = pd.read_csv('data/annotated/data_with_new_annotation_from_peer_review_comments.csv')
    videos_df = pd.read_csv('data/transcriptions/youtube_videos_transcribed_with_metadata.csv')
    videos_df = videos_df[['video_url', 'video_title', 'publish_date']]

    new_columns_order = ['video_url', 'video_title', 'publish_date', 'brazilian_state', 'text_origin',
        'corrected_transcription', 'specific_contexts', 'punchlines',
       'fun', 'humor', 'nonsense', 'wit', 'irony', 'satire', 'sarcasm',
       'cynicism', 'joke_explanation']
    final_df = pd.merge(annotated_df, videos_df, on='video_url', how='left')
    final_df = final_df[new_columns_order]

    final_df = final_df.drop_duplicates()
    final_df = final_df.apply(lambda x: x.str.strip() if x.dtype == "string" else x)

    os.makedirs('data/completed', exist_ok=True)
    final_df.to_csv('data/completed/brazilian_ne_annotated_humorous_texts.csv', index=False)

extract_audios_from_youtube_videos()
extract_transcripts_from_youtube_videos()

'''
The function below should only be executed after the database annotations have been completed
and saved in the folder "data/annotated" with the filename "data_with_new_annotation_from_peer_review_comments.csv".
'''
organize_final_dataset()