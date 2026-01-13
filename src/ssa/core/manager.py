from src.ssa.core.document import Document
from src.ssa.core.embedder import DocumentEmbedder
from src.ssa.ml.tfidf_engine import TfidfEngine
from src.ssa.ml.sumrize import DocumentSummarzer
from src.ssa.ml.features import extract_difficulty_features
from src.ssa.ml.difficulty_classifier import Difficulty_classifier
from src.ssa.ml.transformer_embedder import TransformerEmbedder
import numpy as np
import pandas as pd
from collections import Counter
try:
    import gensim.downloader as api
    from sklearn.metrics.pairwise import cosine_similarity
    GENSIM_AVAILABLE = True
except ImportError:
    print(" gensim not installed run: pip install gensim")
    GENSIM_AVAILABLE = False
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import json
class DocumentManager:
    def __init__(self, storage_file="documents.json"):
        self.storage_file = storage_file
        self.documents = []
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        self.kmeans = None
        self.tfidf_engine = TfidfEngine()
        self._load_initial_documents()
    def predict_document_type(self, content):
        if not hasattr(self, "doc_type_pipeline"):
            print("X Model not traind yet.")
            return None
        return self.doc_type_pipeline.predict([content])[0]
    def add_summarizer(self):
        try:
            self.add_summarizer =  DocumentSummarzer()
            return True
        except:
            print("Install trasformers: pip install transformers")
            return False
    def get_summary(self, doc_index: int) -> str:
        if not hasattr(self, 'summarizer'):
            return "summarizer not avilable"
        
        if 0 <= doc_index < len(self.documents):
            doc = self.documents[doc_index]
            summary = self.summarizer.summarize_document(doc)
            return summary or  "could not generate summary"
        
        return "Invalid document index"
    def predict_difficulty(self, content):
        temp_doc = Document (
            title = "temp",
            content = content,
            file_path="",
            ingestion_date="",
            document_type=None
        )
        features = [temp_doc.extract_difficulty_features()]
        prediction = self.diff_classifier.predict(features)

        return prediction[0]
    def vectorize_documents(self):
        self.tfidf_engine.vectorize(self.documents)

    def cluster_documents(self, n_clusters=3):
        self.tfidf_engine.cluster(self.documents, n_clusters)

    def show_clusters(self):
        self.tfidf_engine.show_clusters(self.documents)

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
    def get_related_documents(self, document_index):
        if document_index >= len(self.documents):
            return []
        
        target_cluster = self.documents[document_index].cluster_id

        related = [
            doc.title
            for doc in self.documents
            if doc.cluster_id == target_cluster
            and doc != self.documents[document_index]
        ]
        return related
    def init_embedder(self, model_name=None, embedder_type="transformer"):
        if embedder_type == "transformer":
           try:
               from src.ssa.ml.transformer_embedder import TransformerEmbedder
               self.embedder = TransformerEmbedder(
                   model_name or "all-MiniLM-L6-v2"
               )
               print("Transfromer embedder initilaized")
               self.document_vectors = {}
               return True
           except Exception as e:
               print(f"failed to initialize trasformer embedder: {e}")
               return False
        elif embedder_type == "glove":
            if not GENSIM_AVAILABLE:
                print("gensim not available. Install with: pip install gensim")
                return False    

            from src.ssa.core.embedder import DocumentEmbedder
            self.embedder = DocumentEmbedder(
                model_name or "glove-twitter-25"
            )
            print("GloVe embedder initialized")
            self.document_vectors = {}
            return True

        else:
            raise ValueError(f"Unknown embedder type: {embedder_type}")
    def compute_all_embeddings(self):
        if not hasattr(self,'embedder'):
            print("Embedder not initialized. Call init_embedder() first")
            return
        for doc in self.documents:
            vector = self.embedder.document_to_vector(doc.content)
            self.document_vectors[doc.title] = vector
        print(f" Computed embeddings for {len(self.document_vectors) } documents")
    def visualize_cluster(self):
        if not hasattr(self, "tfidf_matrix"):
            print("vectorize document first")
            return
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(self.tfidf_matrix.toarray())

        valid_docs = [doc for doc in self.documents if doc.cluster_id is not None]
        valid_indices = [i for i, doc in enumerate(self.documents) if doc.cluster_id is not None]
        
        if not valid_docs:
            print("No clusters found. Run cluster_documents() first.")
            return

        labels = [doc.cluster_id for doc in valid_docs]
        reduced_valid = reduced[valid_indices]
        plt.figure(figsize=(10,8))
        scatter = plt.scatter(reduced_valid[:, 0], reduced_valid[:, 1], 
                             c=labels, cmap='tab20', alpha=0.7)

        for i, doc in enumerate(valid_docs[:10]):  # Label first 10 only
            plt.annotate(doc.title[:15] + "...", 
                        (reduced_valid[i, 0], reduced_valid[i, 1]),
                        fontsize=8, alpha=0.7)
        
        plt.colorbar(scatter, label='Cluster ID')
        plt.title("Document Topic Clusters (PCA)")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.grid(True, alpha=0.3)
        plt.show()
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
                            document_type=entry.get("document_type")
                        )
                        self.documents.append(doc)
                print(f"Loaded {len(self.documents)} document(s) from storage file.")
            except json.JSONDecodeError:
                print(f"Storage file '{self.storage_file}' is empty or corrupted.")
        else:
            print(f"No storage file found at '{self.storage_file}'. Starting fresh.")

    def prepare_difficlulty_training_data(self):
        X = []
        Y = []
        for i, doc in enumerate(self.documents):
            # TEMPORARY manual labels for learning
            if i == 0:
                doc.difficulty_label = "easy"
            elif i == 1:
                doc.difficulty_label = "medium"
            else:
                doc.difficulty_label = "hard"

            X.append(extract_difficulty_features(doc))
            Y.append(doc.difficulty_label)
        return X, Y
    def train_difficulty_model(self):
        from src.ssa.ml.difficulty_classifier import Difficulty_classifier
        X, y = self.prepare_difficlulty_training_data()

        if len(set(y)) < 2:
            raise ValueError("Need at least 2 difficulty classes to train")

        self.difficulty_model = Difficulty_classifier()
        self.difficulty_model.train(X, y)

    print("✅ Difficulty model trained successfully")
    def predict_difficulty_ml(self, content):
        from src.ssa.core.document import Document
        from src.ssa.ml.features import extract_difficulty_features


        temp_doc = Document(
            title="temp",
            content=content,
            file_path="",
            ingestion_date="",
            document_type=None
        )

        features = [extract_difficulty_features(temp_doc)]
        return self.difficulty_model.predict(features)