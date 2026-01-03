import numpy as np
from typing import List, Tuple


class QARetriever:
    def __init__(self, document_manager):
        self.manager = document_manager
        self.embedder = getattr(document_manager, "embedder", None)
        self.document_vectors = None

    def _ensure_embeddings(self):
        if self.document_vectors is not None:
            return

        if hasattr(self.manager, "document_vectors") and self.manager.document_vectors:
            self.document_vectors = self.manager.document_vectors
        else:
            self.manager.init_embedder()
            self.manager.compute_all_embeddings()
            self.document_vectors = self.manager.document_vectors

    def retrieve_for_question(self, question: str, top_k: int = 3) -> List[Tuple]:
        self._ensure_embeddings()
        q_vec = self.embedder.document_to_vector(question)

        results = []
        for title, vec in self.document_vectors.items():
            score = self._cosine(q_vec, vec)
            results.append((title, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def _cosine(self, a: np.ndarray, b: np.ndarray) -> float:
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get_document_by_title(self, title: str):
        for doc in self.manager.documents:
            if doc.title == title:
                return doc
        return None

    def get_retrieved_documents(self, results):
        docs = []
        for title, score in results:
            doc = self.get_document_by_title(title)
            if doc:
                docs.append((doc, score))
        return docs
