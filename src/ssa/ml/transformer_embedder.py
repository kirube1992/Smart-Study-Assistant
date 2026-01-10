import numpy as np
from sentence_transformers import SentenceTransformer
from numpy.linalg import norm


class TransformerEmbedder:
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.vector_size = self.model.get_sentence_embedding_dimension()

        self.model_dims = {
            "all-MiniLM-L6-v2": 384,
            "all-mpnet-base-v2": 768,
            "paraphrase-MiniLM-L3-v2": 384
        }


        self.vector_size = self.model_dims.get(model_name, 384)


    def encode(self, text: str) -> np.ndarray:
        if not text or len(text.strip()) < 3:
            return np.zeros(self.vector_size)
    
        embedding = self.model.encode(text,convert_to_numpy=True)
        return embedding
    def similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        if vec1 is None or vec2 is None:
            return 0.0
        
        n1 = norm(vec1)
        n2 = norm(vec2)


        if n1 == 0 or n2 == 0:
            return 0.0
        
        return float(np.dot(vec1, vec2) / (n1 * n2))