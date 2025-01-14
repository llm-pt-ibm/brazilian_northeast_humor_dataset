import argparse
import os
from config import DATASET_PATH, LLM_MODELS, DEFAULT_LLM_PARAMS
from dataset_loader import DatasetLoader
from llm_interface import LLMInterface
from llm_prompt_manager import PromptManager
from evaluator import Evaluator
from visualization import Visualization
from json_saver import JSONSaver

def main():
    parser = argparse.ArgumentParser(description="Benchmark para LLMs.")
    parser.add_argument("--models", nargs="+", default=[model["name"] for model in LLM_MODELS])
    args = parser.parse_args()

    loader = DatasetLoader(DATASET_PATH)
    data = loader.load_dataset()

    evaluator = Evaluator()
    all_style_scores = {}
    all_punchline_scores = {}
    all_explanation_scores = {}

    for model_config in LLM_MODELS:
        if model_config["name"] in args.models:
            llm = LLMInterface(model_config)
            model_name = model_config["name"]
            print(f"--- Avaliando modelo: {model_name} ---")

            predicted_styles = {style: [] for style in ["funny", "humor", "nonsense", "wit", "irony", "satire", "sarcasm", "cynicism"]}
            ground_truth_styles = {style: [] for style in predicted_styles.keys()}
            predicted_punchlines = []
            ground_truth_punchlines = []
            predicted_explanations = []
            ground_truth_explanations = []

            for i, row in data.iterrows():
                print(f"Processando exemplo {i + 1}/{len(data)}...")

                for style in predicted_styles.keys():
                    prompt = PromptManager.generate_prompt(style, row)
                    llm_answer = llm.generate(prompt, DEFAULT_LLM_PARAMS)
                    predicted_styles[style].append(llm_answer)
                    ground_truth_styles[style].append(row[style])

                punchline_prompt = PromptManager.generate_prompt("punchlines", row)
                predicted_punchlines.append(llm.generate(punchline_prompt, DEFAULT_LLM_PARAMS))
                ground_truth_punchlines.append(row["punchlines"])

                explanation_prompt = PromptManager.generate_prompt("joke_explanation", row)
                llm_joke_explanation = llm.generate(explanation_prompt, DEFAULT_LLM_PARAMS)
                predicted_explanations.append(llm_joke_explanation)
                ground_truth_explanations.append(row["joke_explanation"])

            style_scores = {
                style: evaluator.evaluate_style_classification(predicted_styles[style], ground_truth_styles[style])
                for style in predicted_styles.keys()
            }
            all_style_scores[model_name] = style_scores

            punchline_score = evaluator.evaluate_punchlines(predicted_punchlines, ground_truth_punchlines)
            all_punchline_scores[model_name] = punchline_score

            explanation_similarity = evaluator.evaluate_jokes_explanation(predicted_explanations, ground_truth_explanations)
            all_explanation_scores[model_name] = sum(explanation_similarity) / len(explanation_similarity)

            results = JSONSaver.prepare_results(model_name, style_scores, punchline_score, all_explanation_scores[model_name])
            JSONSaver.save_results(results, os.path.join("results", model_name, "results.json"))

    Visualization.plot_style_comparison(all_style_scores, os.path.join("results", model_name, "style_comparison.png"))
    Visualization.plot_punchline_results(all_punchline_scores, os.path.join("results", model_name, "punchline_results.png"))
    Visualization.plot_explanation_similarity(all_explanation_scores, os.path.join("results", model_name, "explanation_similarity.png"))

if __name__ == "__main__":
    main()
