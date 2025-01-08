import argparse
from src.model_runner import ModelRunner
from src.data_handler import DataHandler
from src.evaluator import Evaluator

def main():
    # Configuração de argumentos do terminal
    parser = argparse.ArgumentParser(description="Benchmark de LLMs")
    parser.add_argument("--config", type=str, required=True, help="Caminho do arquivo de configuração dos modelos")
    parser.add_argument("--data", type=str, required=True, help="Caminho do dataset de entrada")
    parser.add_argument("--output", type=str, required=True, help="Caminho do diretório para salvar os resultados")
    args = parser.parse_args()

    # Carrega os dados e configurações
    data_handler = DataHandler(args.data)
    dataset = data_handler.load_data()

    # Inicializa os modelos
    model_runner = ModelRunner(args.config)

    # Executa os prompts
    evaluator = Evaluator(model_runner, dataset, args.output)
    evaluator.run_benchmark()

if __name__ == "__main__":
    main()
