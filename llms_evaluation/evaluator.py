# evaluator.py

from sklearn.metrics import f1_score, classification_report
from rouge_score import rouge_scorer

class Evaluator:
    def evaluate_classification(self, ground_truth, predictions):
        return classification_report(ground_truth, predictions, output_dict=True)
    
    def evaluate_rouge(self, ground_truth, predictions):
        scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
        scores = [scorer.score(gt, pred) for gt, pred in zip(ground_truth, predictions)]
        return scores
