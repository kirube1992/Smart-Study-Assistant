import numpy as np
from sentence_transformers import SentenceTransformer
from numpy.linalg import norm


class TransformerEmbedder:
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.vector_size = self.model.get_sentence_embedding_dimension()
        self.vector_size = self.model_dims.get(model_name, 384)

    def encode(self, text: str) -> np.ndarray:
        if not text or len(text.strip()) < 3:
            return np.zeros(self.vector_size)
    
        return self.model.encode(text,convert_to_numpy=True)
    
    def embed_batch(self, texts):
        return self.model.encode(texts,convert_to_numpy=True)
    def similarity(self, v1, v2) -> float:
        if norm(v1) == 0 or norm(v2) == 0:
            return 0.0
        
        return float(np.dot(v1,v2))/(norm(v1) * norm(v2))
