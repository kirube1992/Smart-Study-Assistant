from sklearn.linear_model import LogisticRegression
import numpy as np

class Difficulty_classifier():
    def __init__(self):
        self.model = LogisticRegression(max_iter=1000)
        self.trained = False
    def train(self, X, y):
        if len(set(y)) < 2:
            raise ValueError("Need at least 2 difficulty classes to train")
        
        self.model.fit(X,y)
        self.trained = True
        print("Diffidculty classifier trained")
    def predict(self, features):
        if not self.trained:
            raise RuntimeError("Model not trained yet")
        features = np.array(features)
        
        return self.model.predict(features)[0]