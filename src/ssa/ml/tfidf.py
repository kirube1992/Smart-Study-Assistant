from sklearn.feature_extraction.text import TfidfVectorizer

class TfidfEngine:
    def __init__(self, max_features=1000, stop_words="english"):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words=stop_words
        )
        self.matrix = None

    def fit_transform(self, texts):
        self.matrix = self.vectorizer.fit_transform(texts)
        return self.matrix
