import numpy as np

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