from datetime import datetime, date
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import json
import os
import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
try:
    import gensim.downloader as api
    from sklearn.metrics.pairwise import cosine_similarity
    GENSIM_AVAILABLE = True
except ImportError:
    print(" gensim not installed run: pip install gensim")
    GENSIM_AVAILABLE = False

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


class Document:
    def __init__(self, title, content, file_path, ingestion_date, document_type):
        self.title = title
        self.content = content
        self.file_path = file_path
        self.ingestion_date = ingestion_date
        self.tokens = [] # need to understund 
        self.document_type = document_type
        self.difficulty_score = 0
        self.difficulty_label = None
        self.cluster_id = None
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
        long_word_ratio = len([w for w in self.tokens if len(w) > 6])/word_count

        self.difficulty_score = (
            ave_word_length * 0.4 + 
            unique_ratio * 8 +
            long_word_ratio * 15 +
            word_count * 0.01
        )

        if self.difficulty_score < 3:
            self.difficulty_label = "easy"
        elif self.difficulty_score < 11:
            self.difficulty_label = "medium"
        else:
            self.difficulty_label = "hard"
        return self.difficulty_label
    def extract_difficulty_features(self):
        if not self.tokens:
            self.preprocess_text()
        word_count = len(self.tokens)
        if word_count == 0:
            return[0,0,0,0]
        avg_word_length = sum(len(w) for w in self.tokens)/word_count
        unique_ratio = len(set(self.tokens)) / word_count
        long_word_ratio = len([w for w in self.tokens if len(w) >6]) /word_count

        return [
            word_count,
            avg_word_length,
            unique_ratio,
            long_word_ratio
        ]
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
    def predict_document_type(self, content):
        if not hasattr(self, "doc_type_pipeline"):
            print("X Model not traind yet.")
            return None
        return self.doc_type_pipeline.predict([content])[0]
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
    def vectorize_documents(self):
        texts = [doc.content for doc in self.documents]

        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=1000
        )

        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        print("Documents vetorized using TF-IDF")

    def  cluster_documents(self, n_clusters=3):
        doc_count = len(self.documents)

        if doc_count < 2:
            print(" Not enough documents to cluster")
            return
        if n_clusters > doc_count:
            n_clusters = doc_count
            print(f"Reduced cluster to{n_clusters}")

        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = self.kmeans.fit_predict(self.tfidf_matrix)

        for doc, label in zip(self.documents, cluster_labels):
            doc.cluster_id = label

        print(f" Document clutered into {n_clusters} topics")
    def show_clusters(self):
        clusters = {}

        for doc in self.documents:
            clusters.setdefault(doc.cluster_id, []).append(doc.title)
        for cluster_id, titles in clusters.items():
            print(f"Cluster {cluster_id}:")
            for title in titles:
                    print(f" -{title}")
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
    def init_embedder(self, model_name='glove-twitter-25'):
        if not GENSIM_AVAILABLE:
            print("gensim not available. Install with: pip install gensim")
            return False
        self.embedder = DocumentEmbedder(model_name)
        self.document_vectors = {}
        print("Document embedder initialized")
        return True
    def compute_all_embeddings(self):
        if not hasattr(self,'embedder'):
            print("Embedder not initialized. Call init_embedder() first")
            return
        for doc in self.documents:
            vector = self.embedder.document_to_vector(doc.content)
            self.document_vectors[doc.title] = vector
        print(f" Computed embeddings for {len(self.document_vectors) } documents")
    def find_similar_documents(self, query_doc_title, top_n=3):
        if not hasattr(self, 'document_vectors'):
            print("❌ No embeddings computed. Call compute_all_embeddings() first")
            return []
        if query_doc_title not in self.document_vectors:
            print(f"❌ Document '{query_doc_title}' not found")
            return []
        query_vector = self.document_vectors[query_doc_title]
        results = []
        for title, vector in self.document_vectors.items():
            if title == query_doc_title:
                continue
            similarity = self._cosine_similarity(query_vector, vector)
            results.append((title, similarity))
        results.sort(key=lambda x:x[1], reverse=True)

        return results[:top_n]
    def find_similar_by_content(self, content, top_n=3):
        if not hasattr(self, 'embedder'):
            print("❌ Embedder not initialized. Call init_embedder() first")
            return []
        if not hasattr(self, 'document_vectors'):
            print("❌ No embeddings computed. Computing now...")
            self.compute_all_embeddings()

        results = []
        query_vector = self.embedder.document_to_vector(content)

        if query_vector is None:
            return []
        
        for title, vector in self.document_vectors.items():
            similarity = self._cosine_similarity(query_vector, vector)
            results.append((title, similarity))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]
        
    def _cosine_similarity(self, vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product/(norm1 * norm2)
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
