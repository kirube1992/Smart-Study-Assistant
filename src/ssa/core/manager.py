from src.ssa.core.document import Document
from src.ssa.core.embedder import DocumentEmbedder
from src.ssa.ml.tfidf_engine import TfidfEngine
from typing import List, Dict, Optional, Any
from src.ssa.ml.semantic_summarizer import SemanticSummarizer  
from src.ssa.ml.features import extract_difficulty_features
from src.ssa.ml.difficulty_classifier import Difficulty_classifier
from src.ssa.ml.transformer_embedder import TransformerEmbedder
from src.ssa.ml.simple_llm import SimpleLLM

from ..ml.flan_t5_client import FlanT5Client
from ..ml.prompt_engineer import PromptEngineer
import numpy as np
import pandas as pd
from collections import Counter
from datetime import datetime
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
               print("Transformer embedder initialized")
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
    def add_summarizer(self):
        try:
            from src.ssa.ml.summarizer import DocumentSummarizer 
            return True
        except:
            print("Install trasformers: pip install transformers")
            return False
    def get_summary(self, doc_index: int, use_semantic: bool = True) -> str:
        if 0 <= doc_index < len(self.documents):
            doc = self.documents[doc_index]
            if use_semantic and hasattr(self, 'semantic_summarizer'):
                summary_data = self.semantic_summarizer.summarize_document(doc)
                return summary_data["summary"] if summary_data else "could not generate semantic summary"
            else:
                return "Summarizer not avilable"
        return "invalid document index"
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
    
    def init_week12_features(self):
        print("🚀 Initializing Week 12 Features...")

        success = self.init_embedder(
            model_name="all-MiniLM-L6-v2",
            embedder_type="transformer"
        )

        if not success:
            print("Failed to initialize transformer embedder")
            return False
        
        print("Creating semantic embeddings.")
        self.compute_all_embeddings()


        try:
            from src.ssa.ml.semantic_summarizer import SemanticSummarizer
            self.semantic_summarizer = SemanticSummarizer(self.embedder)
            print("Semantic summarizer initialized")
        except Exception as e:
            print(f"Failed to initialize semantic summarizer: {e}")
            return 
        print("🎉 Week 12 features initialized successfully!")
        return True  # ✅ Make sure this returns True!
        
    def semantic_search(self, query: str, top_k: int = 5,threshold: float = 0.3):
        if not hasattr(self,'embedder') or not hasattr(self,'document_vectors'):
            print("Semantic search not initialized. call init_week12_feature() first.")
            return []
        query_vector = self.embedder.encode(query)
        results = []
        for title, doc_vector in self.document_vectors.items():

            doc = next((d for d in self.documents if d.title == title), None)
            if not doc:
                continue
            similarity = self.embedder.similarity(query_vector, doc_vector)

            if similarity >= threshold:
                results.append({
                    "document":doc,
                    "title":doc.title,
                    "similarity": similarity,
                    "content_preview": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content
                })

        results.sort(key=lambda x: x["similarity"], reverse=True)

        return results[:top_k]
            
    def answer_question(self, question: str, use_semantic_summary: bool = True) -> Dict:
        # Step 1: Semantic search
        search_results = self.semantic_search(question, top_k=3, threshold=0.25)
        
        if not search_results:
            return {
                "question": question,
                "answer": "I couldn't find relevant information in your study materials.",
                "sources": [],
                "method": "semantic_search"
            }
        
        # Step 2: Generate summaries
        answer_parts = []
        sources = []
        
        for result in search_results:
            doc = result["document"]
            
            if use_semantic_summary and hasattr(self, 'semantic_summarizer'):
                # Use semantic summarizer focused on the question
                summary_data = self.semantic_summarizer.summarize_document(
                    doc, 
                    focus_query=question
                )
                summary = summary_data["summary"]
                summary_type = "semantic"
            elif hasattr(self, 'abstractive_summarizer') and self.abstractive_summarizer:
                # Use abstractive summarizer
                summary = self.abstractive_summarizer.summarize_document(doc)
                summary_type = "abstractive"
            else:
                # Fallback to content preview
                summary = result["content_preview"]
                summary_type = "preview"
            
            answer_parts.append(f"**{doc.title}** (relevance: {result['similarity']:.2f}):\n{summary}")
            
            sources.append({
                "title": doc.title,
                "similarity": result["similarity"],
                "summary_type": summary_type,
                "content_length": len(doc.content)
            })
        
        # Step 3: Combine into final answer
        answer = "\n\n".join(answer_parts)
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "total_documents": len(self.documents),
            "relevant_documents": len(search_results),
            "method": "semantic_search_with_summarization"
        }
    
    def create_semantic_study_guide(self, topic: str, num_documents: int = 5) -> Dict:
        """
        Create a semantic study guide on a specific topic.
        
        Args:
            topic: Topic to create guide about
            num_documents: Number of documents to include
            
        Returns:
            Study guide with summaries
        """
        # Find relevant documents semantically
        search_results = self.semantic_search(topic, top_k=num_documents, threshold=0.2)
        
        guide = {
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "documents": []
        }
        
        for result in search_results:
            doc = result["document"]
            
            # Get semantic summary focused on the topic
            if hasattr(self, 'semantic_summarizer'):
                summary_data = self.semantic_summarizer.summarize_document(doc, focus_query=topic)
                summary = summary_data["summary"]
                compression = summary_data["compression_ratio"]
            else:
                summary = doc.content[:300] + "..." if len(doc.content) > 300 else doc.content
                compression = 1.0
            
            # Extract key points (first few sentences of summary)
            sentences = self.semantic_summarizer._split_into_sentences(summary)
            key_points = sentences[:min(3, len(sentences))]
            
            guide["documents"].append({
                "title": doc.title,
                "relevance_score": result["similarity"],
                "summary": summary,
                "key_points": key_points,
                "compression_ratio": compression,
                "original_length": len(doc.content.split()),
                "summary_length": len(summary.split())
            })
        
        return guide
    
    def compare_search_methods(self, query: str):
        """
        Compare keyword-based (Week 11) vs semantic search (Week 12)
        
        Args:
            query: Search query to compare
        """
        print(f"\n🔍 Comparing Search Methods for: '{query}'")
        print("=" * 60)
        
        # Week 11: Keyword-based search (using your existing AnswerExtractor)
        print("\n📝 Week 11 - Keyword-based Search:")
        print("-" * 40)
        
        try:
            from src.ssa.qa.answer_extractor import AnswerExtractor
            extractor = AnswerExtractor()
            
            # Mock documents for comparison
            mock_docs = [(doc, 1.0) for doc in self.documents]
            keyword_results = extractor.extract_answers(query, mock_docs, max_answers=3)
            
            for i, (answer, score, source) in enumerate(keyword_results[:3], 1):
                print(f"{i}. Score: {score:.3f}")
                print(f"   Source: {source}")
                print(f"   Answer: {answer[:100]}...")
        except Exception as e:
            print(f"   Keyword search not available: {e}")
        
        # Week 12: Semantic search
        print("\n🤖 Week 12 - Semantic Search:")
        print("-" * 40)
        
        semantic_results = self.semantic_search(query, top_k=3)
        
        for i, result in enumerate(semantic_results, 1):
            print(f"{i}. Score: {result['similarity']:.3f}")
            print(f"   Source: {result['title']}")
            print(f"   Preview: {result['content_preview'][:100]}...")
        
        print("\n" + "=" * 60)


        
    def init_llm(self):
        """Initialize LLM (minimal version)"""
        try:
            from ..ml.flan_t5_client import FlanT5Client
            from ..ml.prompt_engineer import PromptEngineer
            
            self.llm = FlanT5Client("small")
            self.prompt_eng = PromptEngineer()
            print("✅ LLM initialized")
            return True
        except ImportError as e:
            print(f"❌ Error: {e}")
            return False

    def answer_with_llm(self, question):
        """Simple LLM Q&A"""
        if not hasattr(self, 'llm'):
            return "LLM not initialized"
        
        # Get relevant documents
        results = self.semantic_search(question, top_k=2, threshold=0.2)
        
        if results:
            # Format context
            context = self.prompt_eng.format_context(results)
            prompt = self.prompt_eng.build_rag_prompt(context, question)
            
            # Generate answer
            answer = self.llm.generate(prompt, max_length=200)
            
            return {
                "question": question,
                "answer": answer,
                "sources": [{"title": r["title"], "score": r["similarity"]} for r in results]
            }
        else:
            return {
                "question": question,
                "answer": "No relevant documents found.",
                "sources": []
            }
    def init_week13(self):
        """Week 13: Initialize DistilGPT2 LLM"""
        print("\n🚀 Week 13: Initializing DistilGPT2 LLM...")
        
        try:
            from transformers import pipeline
            self.gpt2 = pipeline("text-generation", model="distilgpt2")
            print("✅ DistilGPT2 LLM ready!")
            print("   Model: distilgpt2 (82M parameters)")
            print("   Status: Fast & reliable")
            return True
        except Exception as e:
            print(f"❌ LLM error: {e}")
            return False
    
    def ask_gpt2(self, question):
        """Week 13: Simple Q&A with DistilGPT2"""
        if not hasattr(self, 'gpt2'):
            if not self.init_week13():
                return {
                    "question": question,
                    "answer": "LLM not available",
                    "error": True
                }
        
        # Generate answer
        result = self.gpt2(
            f"Question: {question}\nAnswer:",
            max_new_tokens=100,
            temperature=0.8,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.2,
            truncation=True
        )
        
        answer = result[0]['generated_text']
        # Extract answer part
        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()
        elif "Question:" in answer:
            answer = answer.replace(f"Question: {question}", "").strip()
        
        return {
            "question": question,
            "answer": answer,
            "model": "DistilGPT2",
            "week": 13
        }
    
    def ask_llm(self, question, use_context=False):
        """Week 13: Enhanced LLM Q&A with optional context"""
        if not hasattr(self, 'gpt2'):
            if not self.init_week13():
                return {
                    "question": question,
                    "answer": "LLM not available",
                    "error": True
                }
        
        # If use_context is True, incorporate document context
        if use_context and hasattr(self, 'documents') and self.documents:
            # Get relevant documents using semantic search
            search_results = self.semantic_search(question, top_k=2, threshold=0.2)
            
            if search_results:
                # Build context from documents
                context_parts = []
                for result in search_results:
                    doc = result["document"]
                    summary = doc.content[:150] + "..." if len(doc.content) > 150 else doc.content
                    context_parts.append(f"Document: {doc.title}\nContent: {summary}\nRelevance: {result['similarity']:.2f}")
                
                context = "\n\n".join(context_parts)
                prompt = f"Context from study materials:\n{context}\n\nQuestion: {question}\nAnswer based on the context:"
            else:
                prompt = f"Question: {question}\nAnswer:"
        else:
            # Just use the question without context
            prompt = f"Question: {question}\nAnswer:"
        
        # Generate answer
        result = self.gpt2(
            prompt,
            max_new_tokens=150,  # Slightly longer for context
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.2,
            truncation=True
        )
        
        answer = result[0]['generated_text']
        
        # Extract answer part
        if "Answer based on the context:" in answer:
            answer = answer.split("Answer based on the context:")[-1].strip()
        elif "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()
        elif "Question:" in answer:
            answer = answer.replace(f"Question: {question}", "").strip()
        
        return {
            "question": question,
            "answer": answer,
            "model": "DistilGPT2",
            "context_used": use_context,
            "week": 13
        }
    
    # Optional: Add a method for Week 14-style RAG (more advanced)
    def rag_answer(self, question):
        """Week 14 style: RAG with document retrieval"""
        # Step 1: Get relevant documents
        search_results = self.semantic_search(question, top_k=3, threshold=0.2)
        
        if not search_results:
            return self.ask_llm(question, use_context=False)
        
        # Step 2: Build RAG prompt
        context_parts = []
        sources = []
        
        for i, result in enumerate(search_results):
            doc = result["document"]
            # Use summarizer if available
            if hasattr(self, 'semantic_summarizer'):
                summary_data = self.semantic_summarizer.summarize_document(doc, focus_query=question)
                summary = summary_data["summary"]
            else:
                summary = doc.content[:200] + "..." if len(doc.content) > 200 else doc.content
            
            context_parts.append(f"[Source {i+1}] {doc.title}:\n{summary}")
            sources.append({
                "title": doc.title,
                "similarity": result["similarity"]
            })
        
        context = "\n\n".join(context_parts)
        
        # Step 3: Create RAG prompt
        rag_prompt = f"""Based on the following study materials, answer the question.

            Study Materials:
            {context}

            Question: {question}

            Please provide a clear, concise answer based on the materials above. If the information isn't in the materials, say so.

            Answer:"""
        
        # Step 4: Generate answer
        if not hasattr(self, 'gpt2'):
            self.init_week13()
        
        result = self.gpt2(
            rag_prompt,
            max_new_tokens=200,
            temperature=0.5,  # Lower temperature for factual answers
            do_sample=True,
            top_p=0.85,
            repetition_penalty=1.1
        )
        
        answer = result[0]['generated_text']
        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "context_used": True,
            "method": "RAG",
            "week": "13-14 hybrid"
        }