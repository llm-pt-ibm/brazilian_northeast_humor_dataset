import gc
import os
import pandas as pd
import torch

from bode_model import *
from cabrita_model import *
from granite_model import *
from yt_audio_extractor import *
from yt_video_transcriber import *

def extract_audios_from_youtube_videos():
    yt_audio_extractor = YouTubeAudioExtractor()
    yt_videos = pd.read_csv('data/videos/youtube_videos.csv')
    for video_url in yt_videos['video_url']:
        try:
            yt_audio_extractor.extract_audio_from_youtube_video(video_url, 'data/audios')
            print('Step completed.')
        except Exception as e:
            print(e)
            print(f'Step failed for url {video_url}.')

extract_audios_from_youtube_videos()

def extract_transcripts_from_youtube_videos():
    yt_transcriber = YouTubeVideoTranscriber()
    yt_transcriber.transcribe_youtube_videos()

def evaluate_transcripts():
    models = [BodeModel(), GraniteModel()]#, CabritaModel()]

    transcriptions_df = pd.read_csv(os.path.join(os.getcwd(), 'data', 'transcriptions', 'youtube_videos_transcribed.csv'))
    transcriptions = transcriptions_df['transcription'].tolist()

    instruction = 'A entrada a seguir contém uma piada dita por um humorista. Analise o que faz essa piada ser engraçada.'
    new_df = pd.DataFrame(columns = ['transcription', 'instruction', 'model_result', 'model_name'])

    for model in models:
        model_name = model.get_model_name()
        for transcription in transcriptions:
                if transcription is not None and str(transcription).strip() not in ('', 'nan'):
                    print(f'Step started.')
                    model_result = model.evaluate(instruction = instruction,input = transcription)
                    print(f'Step completed.')

                    new_row = {'transcription': transcription, 'instruction': instruction, 'model_result': model_result, 'model_name': model_name}
                    new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)

        del model
        gc.collect()
        torch.cuda.empty_cache()

        new_df.to_csv(os.path.join(os.getcwd(), 'data', 'evaluations', 'transcripts_evaluation.csv'), index=False)

