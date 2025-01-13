# Caminho do dataset
DATASET_PATH = "/home/josegama/Documentos/GitHub/humor_experiments-1/llms_evaluation/data/transcripted_humor_videos.csv"

# Configuração padrão para os modelos
DEFAULT_LLM_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 256
}

# Modelos a serem avaliados
LLM_MODELS = [
    #{"name": "OpenAI GPT-4", "type": "api", "endpoint": "https://api.openai.com/v1/chat/completions", "api_key": "your_api_key"},
    {"name": "GOOGLE FLAN T5 BASE", "type": "hf", "model_name": "google/flan-t5-base"}
]

# Colunas do dataset
COLUMNS = [
    "corrected_transcription",
    "text_origin",
    "specific_contexts",
    "punchlines",
    "funny",
    "humor",
    "nonsense",
    "wit",
    "irony",
    "satire",
    "sarcasm",
    "cynicism",
    "joke_explanation"
]
