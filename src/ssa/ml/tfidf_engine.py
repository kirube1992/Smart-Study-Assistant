from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

class  TfidfEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=100
         )
        self.tfidf_matrix = None
    def vectorize(self, documents):
            texts = [doc.content for doc in documents]

            if not texts:
                raise ValueError("No documents to vectorize")

            self.tfidf_vectorizer = TfidfVectorizer(
                stop_words="english",
                max_features=1000
            )

            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            print("Documents vetorized using TF-IDF")
            return self.tfidf_matrix
    def  cluster(self,documents, n_clusters=3):
            if self.tfidf_matrix is None:
                raise RuntimeError("Call vectorize() first")
            
            doc_count = len(documents)

            if doc_count < 2:
                print(" Not enough documents to cluster")
                return
            if n_clusters > doc_count:
                n_clusters = doc_count
                print(f"Reduced cluster to{n_clusters}")

            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            labels = kmeans.fit_predict(self.tfidf_matrix)

            for doc, label in zip(documents, labels):
                doc.cluster_id = label

            print(f" Document clutered into {n_clusters} topics")
    def show_clusters(self, documents):
            clusters = {}

            for doc in documents:
                clusters.setdefault(doc.cluster_id, []).append(doc.title)
            for cluster_id, titles in clusters.items():
                print(f"Cluster {cluster_id}:")
                for title in titles:
                        print(f" -{title}")
    print("🔥 USING NEW TFIDF ENGINE 🔥")