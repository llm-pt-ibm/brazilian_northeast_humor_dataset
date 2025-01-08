import pandas as pd
from pathlib import Path

class Evaluator:
    def __init__(self, model_runner, dataset, output_dir):
        self.model_runner = model_runner
        self.dataset = dataset
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_benchmark(self):
        results = []
        for index, row in self.dataset.iterrows():
            punchlines = self._evaluate_punchlines(row)
            styles = self._evaluate_styles(row)
            explanation = self._evaluate_explanation(row)

            results.append({
                "corrected_transcription": row["corrected_transcription"],
                "punchlines": punchlines,
                "styles": styles,
                "explanation": explanation
            })

        output_path = self.output_dir / "results.csv"
        pd.DataFrame(results).to_csv(output_path, index=False)
        print(f"Resultados salvos em {output_path}")

    def _evaluate_punchlines(self, row):
        prompt = self._load_prompt("punchlines_prompt.txt").format(text=row["corrected_transcription"])
        return self.model_runner.run_prompt("gpt-4", prompt, {"temperature": 0.7, "max_tokens": 500})

    def _evaluate_styles(self, row):
        prompt = self._load_prompt("styles_prompt.txt").format(text=row["corrected_transcription"])
        return self.model_runner.run_prompt("gpt-4", prompt, {"temperature": 0.7, "max_tokens": 500})

    def _evaluate_explanation(self, row):
        prompt = self._load_prompt("explanation_prompt.txt").format(text=row["corrected_transcription"])
        return self.model_runner.run_prompt("gpt-4", prompt, {"temperature": 0.7, "max_tokens": 500})

    def _load_prompt(self, prompt_file):
        with open(f"prompts/{prompt_file}", "r") as file:
            return file.read()
