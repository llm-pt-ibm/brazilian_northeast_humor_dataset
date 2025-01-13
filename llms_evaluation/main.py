import argparse
from config import DATASET_PATH, LLM_MODELS, DEFAULT_LLM_PARAMS
from dataset_loader import DatasetLoader
from llm_interface import LLMInterface
from llm_prompt_manager import PromptManager
from evaluator import Evaluator
from visualization import Visualization

def main():
    parser = argparse.ArgumentParser(description="Benchmark para LLMs.")
    parser.add_argument("--models", nargs="+", default=[model["name"] for model in LLM_MODELS])
    args = parser.parse_args()

    # Carrega o dataset
    loader = DatasetLoader(DATASET_PATH)
    data = loader.load_dataset()

    # Inicializa avaliador e resultados globais
    evaluator = Evaluator()
    all_style_scores = {}
    all_punchline_scores = {}
    all_explanation_scores = {}

    for model_config in LLM_MODELS:
        if model_config["name"] in args.models:
            llm = LLMInterface(model_config)
            model_name = model_config["name"]
            print(f"--- Avaliando modelo: {model_name} ---")

            # Prepara listas para armazenar as predições e os valores reais
            predicted_styles = {style: [] for style in ["funny", "humor", "nonsense", "wit", "irony", "satire", "sarcasm", "cynicism"]}
            ground_truth_styles = {style: [] for style in predicted_styles.keys()}
            predicted_punchlines = []
            ground_truth_punchlines = []
            predicted_explanations = []
            ground_truth_explanations = []

            # Loop pelos exemplos no dataset
            for i, row in data.iterrows():
                print(f"Processando exemplo {i + 1}/{len(data)}...")

                # Predições e ground truths para estilos cômicos
                for style in predicted_styles.keys():
                    prompt = PromptManager.generate_prompt(style, row)
                    llm_answer = llm.generate(prompt, DEFAULT_LLM_PARAMS)
                    print(llm_answer)
                    predicted_styles[style].append(llm_answer)
                    ground_truth_styles[style].append(row[style])

                # Predições e ground truths para punchlines
                punchline_prompt = PromptManager.generate_prompt("punchlines", row)
                predicted_punchlines.append(llm.generate(punchline_prompt, DEFAULT_LLM_PARAMS))
                ground_truth_punchlines.append(row["punchlines"])

                # Predições e ground truths para explicações
                explanation_prompt = PromptManager.generate_prompt("joke_explanation", row)
                predicted_explanations.append(llm.generate(explanation_prompt, DEFAULT_LLM_PARAMS))
                ground_truth_explanations.append(row["joke_explanation"])

            # Avaliação de estilos cômicos (média para cada estilo)
            style_scores = {
                style: evaluator.evaluate_style_classification(predicted_styles[style], ground_truth_styles[style])
                for style in predicted_styles.keys()
            }
            all_style_scores[model_name] = style_scores

            # Avaliação de punchlines
            punchline_score = evaluator.evaluate_punchlines(predicted_punchlines, ground_truth_punchlines)
            all_punchline_scores[model_name] = punchline_score

            # Avaliação de explicações
            explanation_similarity = evaluator.evaluate_jokes_explanation(predicted_explanations, ground_truth_explanations)
            all_explanation_scores[model_name] = sum(explanation_similarity) / len(explanation_similarity)

    # Geração dos gráficos
    print("Gerando gráficos...")

    # Gráfico de comparação por estilo cômico
    Visualization.plot_style_comparison(all_style_scores, "style_comparison.png")
    print("Gráfico de estilos cômicos salvo em 'style_comparison.png'.")

    # Gráfico de resultados de punchlines
    Visualization.plot_punchline_results(all_punchline_scores, "punchline_results.png")
    print("Gráfico de punchlines salvo em 'punchline_results.png'.")

    # Gráfico de similaridade de explicações
    Visualization.plot_explanation_similarity(all_explanation_scores, "explanation_similarity.png")
    print("Gráfico de explicações salvo em 'explanation_similarity.png'.")

if __name__ == "__main__":
    main()
