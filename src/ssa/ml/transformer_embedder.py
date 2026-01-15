import numpy as np
from sentence_transformers import SentenceTransformer
from numpy.linalg import norm

class TransformerEmbedder:
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        
        self.model_name = model_name
        self.model = None 
        self.vector_size = None
        self.loaded = False
    def load_model(self):
        try:
            self.model = SentenceTransformer(self.model_name)
            try:
                self.vector_size = self.model.get_sentence_embedding_dimension()
            except Exception:
                # fallback to common size
                self.vector_size = 384
            self.loaded = True
            return True
        except Exception as e:
            print(f"Failed to load transformer model '{self.model_name}': {e}")
            self.loaded = False
            # ensure vector_size is defined to avoid errors elsewhere
            if self.vector_size is None:
                self.vector_size = 0
            return False
    def document_to_vector(self, text: str) -> np.ndarray:
        if not self.loaded:
            if not self.load_model():
                return np.zeros(self.vector_size)
            
        if not text or len(text.strip()) < 3:
            return np.zeros(self.vector_size)
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
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
