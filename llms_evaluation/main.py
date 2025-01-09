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

    # Inicializa avaliadores e visualização
    evaluator = Evaluator()

    for model_config in LLM_MODELS:
        if model_config["name"] in args.models:
            llm = LLMInterface(model_config)

            # Itera sobre o dataset
            for _, row in data.iterrows():
                prompt = PromptManager.generate_prompt("punchlines", row)
                response = llm.generate(prompt, DEFAULT_LLM_PARAMS)
                # Adicione o código para avaliar o resultado aqui

    # Exemplo de visualização
    Visualization.plot_classification_report({"funny": 0.85, "humor": 0.75}, "results.png")

if __name__ == "__main__":
    main()
