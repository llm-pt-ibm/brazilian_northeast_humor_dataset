import matplotlib.pyplot as plt

class Visualization:
    @staticmethod
    def plot_classification_report(report, output_path):
        plt.figure(figsize=(10, 6))
        plt.bar(report.keys(), report.values())
        plt.title("F1-Scores por Estilo Cômico")
        plt.savefig(output_path)
