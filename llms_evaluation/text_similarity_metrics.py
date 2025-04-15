from sentence_transformers import SentenceTransformer, util

class TextSimilarityMetrics:
    def __init__(self):
        pass

    def paraphrase_mpnet_similarity(self, text1, text2):
        """
        Calculate the paraphrase MPNet similarity between two texts.
        """
        model = SentenceTransformer('paraphrase-mpnet-base-v2')
        embeddings1 = model.encode(text1)
        embeddings2 = model.encode(text2)
        cosine_similarity = util.pytorch_cos_sim(embeddings1, embeddings2)
        return cosine_similarity.item()