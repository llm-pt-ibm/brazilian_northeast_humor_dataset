import os
import pandas as pd

from yt_data_extractor import *
from yt_video_transcriber import *

def extract_audios_from_youtube_videos():
    videos_path = 'data/videos/youtube_videos.csv'
    if not os.path.exists(videos_path):
        print(f"[AVISO] Arquivo '{videos_path}' não encontrado. Pulando extração de áudios.")
        return

    print("[INFO] Iniciando extração de áudios dos vídeos do YouTube...")
    yt_data_extractor = YouTubeDataExtractor()

    try:
        yt_videos = pd.read_csv(videos_path)
    except Exception as e:
        print(f"[ERRO] Falha ao ler '{videos_path}': {e}")
        return

    for video_url in yt_videos.get('video_url', []):
        try:
            yt_data_extractor.extract_audio_from_youtube_video(video_url, 'data/audios')
            print(f"[OK] Áudio extraído com sucesso para: {video_url}")
        except Exception as e:
            print(f"[ERRO] Falha ao extrair áudio do vídeo {video_url}.\n{e}")
    print("[INFO] Extração de áudios concluída.")


def extract_transcripts_from_youtube_videos():
    audios_path = 'data/audios'
    if not os.path.exists(audios_path) or not os.listdir(audios_path):
        print(f"[AVISO] Nenhum áudio encontrado em '{audios_path}'. Pulando transcrição.")
        return

    print("[INFO] Iniciando transcrição dos vídeos do YouTube...")
    yt_transcriber = YouTubeVideoTranscriber()

    try:
        yt_transcriber.transcribe_youtube_videos()
        print("[OK] Transcrições concluídas com sucesso.")
    except Exception as e:
        print(f"[ERRO] Falha ao transcrever vídeos do YouTube.\n{e}")


def organize_final_dataset():
    annotated_path = 'data/annotated/data_with_new_annotation_from_peer_review_comments.csv'
    transcribed_path = 'data/transcriptions/youtube_videos_transcribed_with_metadata.csv'

    if not os.path.exists(annotated_path):
        print(f"[AVISO] Arquivo '{annotated_path}' não encontrado. Pulando organização do dataset final.")
        return
    if not os.path.exists(transcribed_path):
        print(f"[AVISO] Arquivo '{transcribed_path}' não encontrado. Pulando organização do dataset final.")
        return

    print("[INFO] Iniciando organização do dataset final...")

    try:
        annotated_df = pd.read_csv(annotated_path)
        videos_df = pd.read_csv(transcribed_path)
    except Exception as e:
        print(f"[ERRO] Falha ao ler arquivos necessários: {e}")
        return

    try:
        videos_df = videos_df[['video_url', 'video_title', 'publish_date']]

        new_columns_order = [
            'video_url', 'video_title', 'publish_date', 'brazilian_state', 'text_origin',
            'corrected_transcription', 'specific_contexts', 'punchlines', 'fun', 'humor',
            'nonsense', 'wit', 'irony', 'satire', 'sarcasm', 'cynicism', 'joke_explanation'
        ]

        final_df = pd.merge(annotated_df, videos_df, on='video_url', how='left')
        final_df = final_df[new_columns_order]

        binary_columns = ['fun', 'humor', 'nonsense', 'wit', 'irony', 'satire', 'sarcasm', 'cynicism']
        for col in binary_columns:
            final_df[col] = final_df[col].map({'Sim': 1, 'Não': 0}).astype('Int64')

        final_df = final_df.drop_duplicates()
        final_df = final_df.apply(lambda x: x.str.strip() if x.dtype == "string" else x)

        os.makedirs('data/completed', exist_ok=True)
        output_path = 'data/completed/brazilian_ne_annotated_humorous_texts.csv'
        final_df.to_csv(output_path, index=False)

        print(f"[OK] Dataset final organizado e salvo em '{output_path}'.")
    except Exception as e:
        print(f"[ERRO] Falha ao organizar o dataset final.\n{e}")


extract_audios_from_youtube_videos()
extract_transcripts_from_youtube_videos()

'''
A função abaixo só deve ser executada após a conclusão das anotações,
salvas no arquivo "data/annotated/data_with_new_annotation_from_peer_review_comments.csv".
'''
organize_final_dataset()
