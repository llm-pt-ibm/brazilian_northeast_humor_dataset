from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity

class Evaluator:
    def __init__(self):
        pass

    def evaluate_punchlines(self, predicted_punchlines_rows, ground_truth_punchlines_rows):
        """
        Avalia a correspondência entre os punchlines previstos e os punchlines do ground truth.
        Utiliza o ROUGE-L como base.
        """
        scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
        rouge_l_scores = []

        for predicted, ground_truth in zip(predicted_punchlines_rows, ground_truth_punchlines_rows):
            score = scorer.score(predicted, ground_truth)
            rouge_l_scores.append(score["rougeL"].fmeasure)
        
        return sum(rouge_l_scores) / len(rouge_l_scores) if rouge_l_scores else 0.0

    def evaluate_style_classification(self, predicted_list, ground_truth_list):
        """
        Compara as previsões com o ground truth para estilos cômicos.
        Retorna a média da correspondência entre as previsões e os valores reais.
        """
        matches = []

        for predicted, ground_truth in zip(predicted_list, ground_truth_list):
            matches.append(int(predicted.lower() == ground_truth.lower()))
        
        return sum(matches) / len(matches) if matches else 0.0

    def evaluate_jokes_explanation(self, model_explanations, ground_truth_explanations):

        model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        similarities = []

        for model_explanation, ground_truth_explanation in zip(model_explanations, ground_truth_explanations):
            embeddings1 = model.encode(model_explanation.lower(), convert_to_tensor=True)
            embeddings2 = model.encode(ground_truth_explanation.lower(), convert_to_tensor=True)
            similarity = cosine_similarity(embeddings1.unsqueeze(0), embeddings2.unsqueeze(0))
            similarities.append(similarity.item())
        
        return similarities