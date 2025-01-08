import pandas as pd

class DataHandler:
    def __init__(self, data_path):
        self.data_path = data_path

    def load_data(self):
        return pd.read_csv(self.data_path)

    def save_results(self, results, output_path):
        results.to_csv(output_path, index=False)
