from typing import Optional, List, Dict
import numpy as np
import re
from src.ssa.ml.transformer_embedder import TransformerEmbedder


class SemanticSummarizer:

    """
    Improved semantic summarizer with better query focus.
    """
    
    def __init__(self, embedder=None, num_sentences: int = 3):
        if embedder is None:
            from .transformer_embedder import TransformerEmbedder
            self.embedder = TransformerEmbedder(model_name="all-MiniLM-L6-v2")
            self.embedder.load_model()
        else:
            self.embedder = embedder
        
        self.num_sentences = num_sentences
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        if not text:
            return []
        
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Better sentence splitting
        text = text.replace('. ', '.|').replace('? ', '?|').replace('! ', '!|')
        if text.endswith(('.', '?', '!')):
            text += '|'
        
        parts = text.split('|')
        sentences = [p.strip() for p in parts if p.strip() and len(p.strip()) > 10]
        
        return sentences
    def summarize_document(self, document, focus_query: str = None) -> Dict:
        """
        Summarize a Document object with metadata.
        
        Args:
            document: Document object
            focus_query: Optional query to focus the summary on
            
        Returns:
            Dictionary with summary and metadata
        """
        if hasattr(document, 'content'):
            text = document.content
            title = getattr(document, 'title', 'Untitled')
        else:
            text = str(document)
            title = "Document"
        
        # Split into sentences
        sentences = self._split_into_sentences(text)
        
        # Generate summary
        summary = self.summarize(text, focus_query)
        
        # Split summary into sentences
        summary_sentences = self._split_into_sentences(summary)
        
        return {
            "title": title,
            "summary": summary,
            "type": "semantic_extractive",
            "focus_query": focus_query,
            "original_sentences": len(sentences),
            "summary_sentences": len(summary_sentences),
            "compression_ratio": len(summary) / max(len(text), 1)
        }
    def summarize(self, text: str, focus_query: str = None) -> str:
        """
        Generate semantic summary with improved query focus.
        """
        if not text or len(text.strip()) < 50:
            return text.strip() if text else ""
        
        sentences = self._split_into_sentences(text)
        if len(sentences) <= self.num_sentences:
            return ' '.join(sentences)
        
        # Get embeddings
        sentence_embeddings = self.embedder.embed_batch(sentences)
        
        # Calculate similarities
        similarities = []
        
        if focus_query:
            # For query focus, calculate similarity to query
            query_embedding = self.embedder.encode(focus_query)
            
            # Also get document embedding for diversity
            doc_embedding = self.embedder.encode(text)
            
            for i, sent_emb in enumerate(sentence_embeddings):
                # Combine query similarity with document centrality
                query_sim = self.embedder.similarity(query_embedding, sent_emb)
                doc_sim = self.embedder.similarity(doc_embedding, sent_emb)
                
                # Weighted score: 70% query relevance, 30% document importance
                combined_score = 0.7 * query_sim + 0.3 * doc_sim
                similarities.append((combined_score, i, sentences[i]))
        else:
            # General summary: use document centrality
            doc_embedding = self.embedder.encode(text)
            
            for i, sent_emb in enumerate(sentence_embeddings):
                sim = self.embedder.similarity(doc_embedding, sent_emb)
                similarities.append((sim, i, sentences[i]))
        
        # Sort by score
        similarities.sort(reverse=True)
        
        # Get top sentences in original order
        top_indices = sorted([idx for _, idx, _ in similarities[:self.num_sentences]])
        selected_sentences = [sentences[idx] for idx in top_indices]
        
        return ' '.join(selected_sentences)
    
    def summarize_with_scores(self, text: str, focus_query: str = None) -> Dict:
        """
        Return summary with scoring information for debugging.
        """
        if not text or len(text.strip()) < 50:
            return {"summary": text.strip() if text else "", "scores": []}
        
        sentences = self._split_into_sentences(text)
        
        # Get embeddings
        sentence_embeddings = self.embedder.embed_batch(sentences)
        
        # Calculate scores
        scores = []
        
        if focus_query:
            query_embedding = self.embedder.encode(focus_query)
            doc_embedding = self.embedder.encode(text)
            
            for i, sent_emb in enumerate(sentence_embeddings):
                query_sim = self.embedder.similarity(query_embedding, sent_emb)
                doc_sim = self.embedder.similarity(doc_embedding, sent_emb)
                combined = 0.7 * query_sim + 0.3 * doc_sim
                scores.append((combined, query_sim, doc_sim, i, sentences[i]))
        else:
            doc_embedding = self.embedder.encode(text)
            
            for i, sent_emb in enumerate(sentence_embeddings):
                sim = self.embedder.similarity(doc_embedding, sent_emb)
                scores.append((sim, sim, sim, i, sentences[i]))  # Same for all
        
        # Sort and get summary
        scores.sort(reverse=True, key=lambda x: x[0])
        top_indices = sorted([idx for _, _, _, idx, _ in scores[:self.num_sentences]])
        selected_sentences = [sentences[idx] for idx in top_indices]
        
        return {
            "summary": ' '.join(selected_sentences),
            "scores": scores,
            "selected_indices": top_indices
        }