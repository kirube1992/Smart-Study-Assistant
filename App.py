from datetime import datetime, date
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import json
import os
import numpy as np
import pandas as pd
import re  


class Document:
    def __init__(self, title, content, file_path, ingestion_date, document_type):
        self.title = title
        self.content = content
        self.file_path = file_path
        self.ingestion_date = ingestion_date
        self.tokens = []
        self.document_type = document_type
        self.difficulty_score = 0
        self.difficulty_label = None
    def preprocess_text(self):
        text_lower = self.content.lower()
        text = re.sub(r'[^\w\s]', '', text_lower)
        self.tokens = text.split()
        return self.tokens
    def tokens_to_numeric(self):
        if not self.tokens:
            self.preprocess_text()
        
        self.numeric_token = np.array([len(word) for word in self.tokens])
        return self.numeric_token
    def calculate_difficulty(self):
        if not self.tokens:
            self.preprocess_text()

        word_count = len(self.tokens)
        if word_count == 0:
            self.difficulty_label = "easy"
            return self.difficulty_label
        
        ave_word_length = sum(len(w) for w in self.tokens)/word_count
        unique_ratio = len(set(self.tokens))/word_count

        self.difficulty_score = (
            ave_word_length * 0.5 + 
            unique_ratio * 10 +
            word_count * 0.01
        )

        if self.difficulty_score < 6:
            self.difficulty_label = "easy"
        elif self.difficulty_score <10:
            self.difficulty_label = "medium"
        else:
            self.difficulty_label = "hard"
        return self.difficulty_label

    def __str__(self):
        return f"Document title: {self.title}, document filePath: {self.file_path}, date of ingestion: {self.ingestion_date}"
    def __repr__(self):
        return f"{self.title} {self.file_path} {self.ingestion_date}"
    
class DocumentManager:
    def __init__(self, storage_file="documents.json"):
        self.storage_file = storage_file
        self.documents = []
        self._load_initial_documents()
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
        self.vectorizer = CountVectorizer()
        X = self.vectorizer.fit_transform(texts)

        self.classifier = LogisticRegression(max_iter=1000)
        self.classifier.fit(X, labels)

        print("document classifier trained successfully")
    def predict_document_type(self, content):
        if not hasattr(self, "classifier"):
            print("X Model not traind yet.")
            return None
        X = self.vectorizer.transform([content])
        prediction = self.classifier.predict(X)
        return prediction[0]
    def analyze_difficulty(self):
        for doc in self.documents:
            label = doc.calculate_difficulty()
            print(f"{doc.title}: {label} (score={doc.difficulty_score:.2f})")
    def to_dataframe(self):
        if not self.documents:
            print('No documents avilabel')
            return None
        data = []
        
        for doc in self.documents:
            tokens = doc.preprocess_text()

            data.append({
             "title": doc.title,
             "file_path": doc.file_path,
             "ingestion_date": doc.ingestion_date,
             "word_count": len(tokens),
             "content": doc.content
            })

        df = pd.DataFrame(data)
        return df
    def analytics_dashboard(self):
        df = self.to_dataframe()
        if df is None:
            return
        print(f'total documents:{len(df)}')
        print(f"average word count:{df['word_count'].mean():.2f}")
        all_words = []
        for document in self.documents:
            if not document.tokens:
                document.preprocess_text()
            all_words.extend(document.tokens)
        common_words = Counter(all_words).most_common(5)
        for word, count in common_words:
            print(f"{word}:{count}")

    def add_document(self,):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    data = json.load(f)
                    for entry in data:
                        if not any(doc.file_path == entry["file_path"] for doc in self.documents):
                            doc = Document(
                                title=entry["title"],
                                content=entry["content"],
                                file_path=entry["file_path"],
                                ingestion_date=entry["ingestion_date"],
                                document_type=None
                            )
                            self.documents.append(doc)
                print(f"Loaded {len(self.documents)} document(s) from {self.storage_file}.")
            except json.JSONDecodeError:
                print(f"Warning: {self.storage_file} is empty or malformed. Starting fresh.")
                self.documents = []
        else:
            print(f"No existing storage file '{self.storage_file}' found. Starting fresh.")
    def list_documents(self):
        if not self.documents:
            print('No documents is found')
        else:
            print("\n--- Current Documents ---")
            for i,  doc in enumerate(self.documents):
                print(f"{i+1}.{doc}")
            print("-------------------------\n")
    
    def save_to_json(self,file_name, append=False):
        # data = [doc.__dict__ for doc in self.documents]

        if append and os.path.exists(file_name):
            with open(file_name,"r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
            existing_path = {item.get("file_path") for item in data}
            for doc in self.documents:
                if doc.file_path not in existing_path:
                   data.append(doc.__dict__)
        else: 
            data = [doc.__dict__ for doc in self.documents]
        with open(file_name,"w") as f:
            json.dump(data,f,indent=4)
        print(f"Saved {len(self.documents)} document(s) to {file_name}")

    def load_from_json(self, file_name):
        if  not os.path.exists(file_name):
            print('No json file found')
            return
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
                for entry in data:
                    doc = Document(
                        title=entry["title"],
                        content=entry["content"],
                        file_path=entry["file_path"],
                        ingestion_date=entry["ingestion_date"]
                    )
                    self.documents.append(doc)
        except Exception as e:
            print(f"Error loading json {e}")

    def _load_initial_documents(self):
        """Private method to load documents on initialization."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    data = json.load(f)
                    for entry in data:
                        # Handle both "Content" and "content" for backward compatibility
                        content = entry.get("content") or entry.get("Content", "")
                        
                        doc = Document(
                            title=entry.get("title", ""),
                            content=content,
                            file_path=entry.get("file_path", ""),
                            ingestion_date=entry.get("ingestion_date", ""),
                            document_type=None
                        )
                        self.documents.append(doc)
                print(f"Loaded {len(self.documents)} document(s) from storage file.")
            except json.JSONDecodeError:
                print(f"Storage file '{self.storage_file}' is empty or corrupted.")
        else:
            print(f"No storage file found at '{self.storage_file}'. Starting fresh.")


# manager = DocumentManager("documents.json")

# manager.documents[0].document_type = "notes"
# manager.documents[1].document_type = "article"

# manager.train_document_classifier()
# # Test prediction
# test_text = "This lecture explains machine learning fundamentals"
# result = manager.predict_document_type(test_text)

# print("Predicted document type:", result)
manager = DocumentManager("documents.json")
manager.analyze_difficulty()
