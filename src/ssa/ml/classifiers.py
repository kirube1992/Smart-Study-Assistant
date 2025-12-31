from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

def train_document_classifier(self):
    texts = []
    labels = []
    for doc in self.documents:
        if doc.document_type is None:
            continue
        texts.append(doc.content)
        labels.append(doc.document_type)
    if len(set(labels)) < 2:
        print("❌ Need at least two document types to train.")
        return
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            stop_words="english",
            max_features=2000
        )),
        ("clf", LogisticRegression(max_iter=1000))
        ])

    param_grid = {
        "tfidf__max_features": [500,1000,2000],
        "tfidf__ngram_range":[(1,1),(1,2)],
        "clf__C":[0.1,1,10]
    }


    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=2,
        scoring="accuracy",
        n_jobs=-1
    )

    grid_search.fit(texts, labels)

    self.doc_type_pipeline = grid_search.best_estimator_ 

    print("Best parpameters found")
    print(grid_search.best_params_)
    print(f"Besr cross-validation accuracy:{grid_search.best_score_:2f}")

def train_difficulty_classifier(self):
    x = []
    y = []

    for doc in self.documents:
        if doc.difficulty_label is None:
            doc.calculate_difficulty()

        x.append(doc.extract_difficulty_features())
        y.append(doc.difficulty_label)
            
    if len(set(y)) < 2:
        print("X not enough difficulty classes to train.")
        return
        
    self.diff_classifier = LogisticRegression(max_iter = 1000)
    self.diff_classifier.fit(x,y)

    print(" Difficulty calssifer trained")
