import os
import matplotlib.pyplot as plt
import seaborn as sns

class Visualization:
    @staticmethod
    def plot_style_comparison(style_scores, output_path):
        """
        Gera um gráfico comparando os desempenhos para cada estilo cômico.
        """
        plt.figure(figsize=(12, 7))
        for model_name, scores in style_scores.items():
            sns.lineplot(x=list(scores.keys()), y=list(scores.values()), marker="o", label=model_name)
        plt.title("Comparação de Desempenho por Estilo Cômico")
        plt.xlabel("Estilos Cômicos")
        plt.ylabel("Pontuação de Estilo")
        plt.xticks(rotation=45)
        plt.legend(title="Modelos")
        plt.tight_layout()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()

    @staticmethod
    def plot_punchline_results(punchline_scores, output_path):
        """
        Gera um gráfico de barras para as pontuações de punchlines por modelo.
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(punchline_scores.keys()), y=list(punchline_scores.values()), palette="coolwarm")
        plt.title("Resultados dos Punchlines")
        plt.xlabel("Modelos")
        plt.ylabel("Pontuação Média de ROUGE-L")
        plt.tight_layout()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()

    @staticmethod
    def plot_explanation_similarity(explanation_scores, output_path):
        """
        Gera um gráfico de barras para as similaridades das explicações por modelo.
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(explanation_scores.keys()), y=list(explanation_scores.values()), palette="crest")
        plt.title("Similaridade Média das Explicações")
        plt.xlabel("Modelos")
        plt.ylabel("Similaridade Média (Cosseno)")
        plt.tight_layout()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)        
        plt.savefig(output_path)
        plt.close()
