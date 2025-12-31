from src.ssa.core.document import Document

try:
    import gensim.downloader as api
    from sklearn.metrics.pairwise import cosine_similarity
    GENSIM_AVAILABLE = True
except ImportError:
    print(" gensim not installed run: pip install gensim")
    GENSIM_AVAILABLE = False
import numpy as np
class DocumentEmbedder:

    def __init__(self, model_name="glove-twitter-25"):
        self.model = None
        self.model_name = model_name
        self.vector_size =None
        self.loaded = False
        self.load_falied = False


        self.model_sizes = {
            "glove-twitter-25": 25,
            "glove-twitter-50": 50,
            "glove-twitter-25": 100,
            "glove-twitter-50": 200,
            "word2vec-google-news-300": 300
            }
        if model_name in self.model_sizes:
            self.vector_size = self.model_sizes[model_name]
        else:
            self.vector_size = 25
    def load_model(self):
        if not GENSIM_AVAILABLE:
            print(" Gensim not available. Install with: pip install gensim")
            return False
        if self.model is None:
            print(f"Loading {self.model_name}.. (first time may take 1-2 minutes)")

            try:
                self.model = api.load(self.model_name)
                self.vector_size = self.model.vector_size
                self.loaded = True
                print(f"Loaded! Vocabulary: {len(self.model):,} words, Vector size: {self.vector_size}")
                return True
            except Exception as e:
                print(f"Faild to load model: {e}")
                return False
        print("model already loaded")
        return True
    def document_to_vector(self, text):

        if not self.loaded or self.model is None:
            if not self.load_model():
                print("Model not loaded. Using zero vector as fallback.")
                if self.vector_size:
                    return np.zeros(self.vector_size)
                else:
                    return np.zeros(25)
            
        words = str(text).lower().split()
        vectors = []

        for word in words:
            if word in self.model:
                vectors.append(self.model[word])

        if not vectors:
            return np.zeros(self.vector_size)
        
        return np.mean(vectors, axis=0)
    def get_word_vector(self, word):
        if not self.load_model():
            return None
        
        word = str(word).lower().strip()
        if word in self.model:
            return self.model[word]
        return np.zeros(self.vector_size)