import pandas as pd

class DatasetLoader:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_dataset(self):
        columns_to_check = [
        "corrected_transcription",
        "text_origin",
        "punchlines",
        "funny",
        "humor",
        "nonsense",
        "wit",
        "irony",
        "satire",
        "sarcasm",
        "cynicism",
        "joke_explanation"]

        dataframe = pd.read_csv(self.file_path)
        filtered_df = dataframe.dropna(subset=columns_to_check)[2:3]

        return filtered_df
