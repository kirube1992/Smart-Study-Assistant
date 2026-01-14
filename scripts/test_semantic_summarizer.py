# File: scripts/week12_final_demo.py

from src.ssa.core.manager import DocumentManager
from src.ssa.core.document import Document
import json

def create_sample_documents():
    """Create sample study documents for testing"""
    return [
        Document(
            title="Machine Learning Fundamentals",
            content="""
            Machine learning is a subset of artificial intelligence that enables systems 
            to learn and improve from experience without being explicitly programmed. 
            It focuses on the development of computer programs that can access data and 
            use it to learn for themselves. There are three main types of machine learning: 
            supervised learning, unsupervised learning, and reinforcement learning. 
            Supervised learning uses labeled datasets to train algorithms. 
            Unsupervised learning finds patterns in unlabeled data. 
            Reinforcement learning uses rewards and penalties to guide learning.
            """,
            file_path="ml_fundamentals.txt",
            ingestion_date="2024-01-01",
            document_type="study_note"
        ),
        Document(
            title="Neural Networks Overview",
            content="""
            Artificial neural networks are computing systems inspired by biological 
            neural networks. They consist of layers of interconnected nodes called neurons. 
            Each neuron processes signals using an activation function. 
            Deep learning uses neural networks with many layers to learn complex patterns. 
            Common architectures include convolutional neural networks for image processing 
            and recurrent neural networks for sequential data like text or time series.
            """,
            file_path="neural_networks.txt",
            ingestion_date="2024-01-01",
            document_type="study_note"
        ),
        Document(
            title="Natural Language Processing Basics",
            content="""
            Natural Language Processing (NLP) is a subfield of artificial intelligence 
            that focuses on the interaction between computers and human language. 
            It enables computers to understand, interpret, and generate human language. 
            Applications include machine translation, sentiment analysis, and chatbots. 
            Modern NLP uses transformer models like BERT and GPT for state-of-the-art results. 
            Tokenization is the process of breaking text into words or subwords.
            """,
            file_path="nlp_basics.txt",
            ingestion_date="2024-01-01",
            document_type="study_note"
        )
    ]

def week12_final_demo():
    """Final Week 12 Demonstration"""
    print("=" * 70)
    print("🤖 SMART STUDY ASSISTANT - WEEK 12 FINAL DEMO")
    print("=" * 70)
    
    # Initialize DocumentManager
    manager = DocumentManager()
    
    # Add sample documents
    print("\n📚 Loading sample study materials...")
    sample_docs = create_sample_documents()
    manager.documents = sample_docs
    print(f"✅ Loaded {len(manager.documents)} documents")
    
    # Initialize Week 12 features
    print("\n🚀 Initializing Week 12 features...")
    if not manager.init_week12_features():
        print("❌ Failed to initialize Week 12 features")
        return
    
    print("\n" + "=" * 70)
    print("1. SEMANTIC SEARCH DEMONSTRATION")
    print("=" * 70)
    
    # Test semantic search
    test_queries = [
        "What is machine learning?",
        "Explain neural networks",
        "How do computers understand language?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results = manager.semantic_search(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result['title']} (Score: {result['similarity']:.3f})")
    
    print("\n" + "=" * 70)
    print("2. SEMANTIC Q&A WITH SUMMARIZATION")
    print("=" * 70)
    
    # Test semantic Q&A
    questions = [
        "What are the types of machine learning?",
        "What are neural networks inspired by?",
        "What is NLP used for?"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        answer_data = manager.answer_question(question, use_semantic_summary=True)
        
        print(f"   Answer preview: {answer_data['answer'][:150]}...")
        print(f"   Sources found: {len(answer_data['sources'])}")
        
        # Show debug info for first source
        if answer_data['sources']:
            first_source = answer_data['sources'][0]
            if 'debug' in first_source and 'top_scores' in first_source['debug']:
                print(f"   Semantic scores for '{first_source['title']}':")
                for sent_idx, score in first_source['debug']['top_scores']:
                    print(f"      Sentence {sent_idx}: {score:.3f}")
    
    print("\n" + "=" * 70)
    print("3. COMPARISON: WEEK 11 vs WEEK 12")
    print("=" * 70)
    
    # Compare search methods
    print("\n🔍 Searching for: 'learning from data'")
    
    # Week 12: Semantic search
    print("\n🤖 Week 12 - Semantic Search:")
    semantic_results = manager.semantic_search("learning from data", top_k=2)
    for i, result in enumerate(semantic_results, 1):
        print(f"   {i}. {result['title']} (Score: {result['similarity']:.3f})")
        print(f"      Preview: {result['content_preview'][:80]}...")
    
    # Week 11: Keyword search (if available)
    print("\n📝 Week 11 - Keyword Search (if implemented):")
    try:
        # Try to use your existing AnswerExtractor
        from src.ssa.qa.answer_extractor import AnswerExtractor
        extractor = AnswerExtractor()
        mock_docs = [(doc, 1.0) for doc in manager.documents]
        keyword_results = extractor.extract_answers("learning from data", mock_docs, max_answers=2)
        
        for i, (answer, score, source) in enumerate(keyword_results, 1):
            print(f"   {i}. Source: {source} (Score: {score:.3f})")
            print(f"      Answer: {answer[:80]}...")
    except:
        print("   (Keyword search not available for comparison)")
    
    print("\n" + "=" * 70)
    print("4. EXPORT SEMANTIC STUDY GUIDE")
    print("=" * 70)
    
    # Create and export study guide
    print("\n📚 Creating semantic study guide on 'Artificial Intelligence'...")
    
    # Find relevant documents
    relevant_docs = manager.semantic_search("Artificial Intelligence", top_k=3, threshold=0.2)
    
    guide = {
        "topic": "Artificial Intelligence",
        "created": "2024-01-01",
        "documents": []
    }
    
    for result in relevant_docs:
        doc = result["document"]
        
        # Get semantic summary focused on AI
        if hasattr(manager, 'semantic_summarizer'):
            summary_data = manager.semantic_summarizer.summarize_with_scores(
                doc.content, 
                focus_query="Artificial Intelligence"
            )
            
            guide["documents"].append({
                "title": doc.title,
                "relevance_score": float(result["similarity"]),
                "summary": summary_data["summary"],
                "key_sentences": [
                    summary_data["scores"][i][4] 
                    for i in summary_data.get("selected_indices", [])
                ]
            })
    
    # Save guide
    guide_file = "semantic_study_guide.json"
    with open(guide_file, 'w') as f:
        json.dump(guide, f, indent=2)
    
    print(f"✅ Study guide saved to: {guide_file}")
    print(f"   Documents included: {len(guide['documents'])}")
    
    print("\n" + "=" * 70)
    print("🎉 WEEK 12 COMPLETE! ✅")
    print("=" * 70)
    
    # Summary
    print("\n📊 WEEK 12 ACHIEVEMENTS:")
    print("   ✓ Semantic embeddings with sentence-transformers")
    print("   ✓ Semantic search (understanding meaning, not keywords)")
    print("   ✓ Semantic summarization (extractive, query-focused)")
    print("   ✓ Integrated Q&A system")
    print("   ✓ Study guide generation")
    print(f"\n📚 Documents processed: {len(manager.documents)}")
    print(f"🤖 Embedding model: {manager.embedder.model_name if hasattr(manager, 'embedder') else 'N/A'}")
    print(f"📝 Summarizer type: {'Semantic + Abstractive' if hasattr(manager, 'abstractive_summarizer') else 'Semantic only'}")

if __name__ == "__main__":
    week12_final_demo()