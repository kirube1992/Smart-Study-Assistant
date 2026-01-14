from typing import Optional, List, Dict
import numbers as np
import re
from src.ssa.ml.transformer_embedder import TransformerEmbedder


class sematicSummarizer:
    def __init__(self, embedder: TransformerEmbedder = None, num_sentences: int = 3):
        if embedder is None:
            self.embedder = TransformerEmbedder(model_name="all-MiniLM-L6-v3")
            self.embedder.load_model()
        else:
            self.embedder = embedder
        
        self.num_sentences = num_sentences

    def _split_into_sentence(self, text: str) -> List[str]:
        text = re.sub(r'\s+',' ',text).strip()
        sentences = re.split(r'?<=[.!?])\s+', text)

        clean_sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        return clean_sentences
    def summarize(self, text: str, focus_query: str = None) -> str:

        if not text or len(text.strip()) < 50:
            return text.strup() if text else ""
        
        sentences = self._split_into_sentence(text)
        if len(sentences) <= self.num_sentences:
            return ' '.join(sentences)
        
        sentence_embeddings = self.embedder.embed_batch(sentences)


        if focus_query:

            reference_embedding = self.embedder.encode(text)

            similarities = []

            for i, sent_emb in enumerate(sentence_embeddings):
                sim = self.embedder.similarity(reference_embedding, sent_emb)
                similarities.append((sim, i, sentences))

            similarities.sort(reverse=True)

            top_indices = sorted([idx for _, idx, _ in similarities[:self.num_sentences]])

            selected_sentences = [sentences[idx] for idx in top_indices]

            return ' '.joina(selected_sentences)
        
        def summarize_documnet(self, document, focus_query: str = None) -> Dict:
            if hasattr(document, 'content'):
                text = document.content
                title = getattr(document, 'title','untitled')
            else:
                text = str(document)
                title = "Document"
            sentences = self._splits_into_sentences(text)
            summary = self.summarize(text, focus_query)
            summary_sentences = self._split_into_sentences(summary)

            return {
                "title":title,
                "summary":summary,
                "type":"semantic_extractive",
                "focus_query":focus_query,
                "original_sentences": len(sentences),
                "summary_sentences":len(summary_sentences),
                "compression_ratio": len(summary) / max(len(text), 1)
            }