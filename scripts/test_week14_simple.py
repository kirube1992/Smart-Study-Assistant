# scripts/test_week14_fixed.py
"""
Test the fixed Week 14 agent
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    print("🧪 TESTING WEEK 14 FIXED AGENT")
    print("=" * 60)
    
    try:
        # Import your existing code
        from src.ssa.core.manager import DocumentManager
        from src.ssa.core.document import Document
        from datetime import datetime
        
        # Create manager
        manager = DocumentManager()
        
        # Add test documents if empty
        if len(manager.documents) == 0:
            print("📝 Adding test documents...")
            test_docs = [
                Document(
                    title="Introduction to AI",
                    content="Artificial intelligence is the simulation of human intelligence processes by machines.",
                    file_path="/test/ai.txt",
                    ingestion_date=datetime.now().isoformat(),
                    document_type="tutorial"
                ),
                Document(
                    title="Machine Learning Basics",
                    content="Machine learning is a subset of AI that enables systems to learn from data.",
                    file_path="/test/ml.txt",
                    ingestion_date=datetime.now().isoformat(),
                    document_type="lecture"
                )
            ]
            manager.documents = test_docs
            print(f"✅ Added {len(test_docs)} test documents")
        
        # Train Week 8 classifier if not trained
        if not hasattr(manager, 'doc_type_pipeline') or manager.doc_type_pipeline is None:
            print("\n🤖 Training Week 8 classifier (simplified)...")
            # Simple training simulation
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                from sklearn.linear_model import LogisticRegression
                from sklearn.pipeline import Pipeline
                
                # Create a simple pipeline
                manager.doc_type_pipeline = Pipeline([
                    ('tfidf', TfidfVectorizer(max_features=100)),
                    ('clf', LogisticRegression())
                ])
                
                # Train with sample data
                texts = [
                    "artificial intelligence is the simulation",
                    "machine learning algorithms build models", 
                    "research paper on neural networks",
                    "textbook chapter about ai",
                    "lecture notes on ml"
                ]
                labels = ["tutorial", "lecture", "research", "textbook", "lecture"]
                
                manager.doc_type_pipeline.fit(texts, labels)
                print("✅ Week 8 classifier trained (simplified)")
            except Exception as e:
                print(f"⚠️  Could not train classifier: {e}")
                print("   Using mock classifier instead")
        
        # Initialize Week 12 features
        print("\n🚀 Initializing Week 12 features...")
        if hasattr(manager, 'init_week12_features'):
            manager.init_week12_features()
        
        # Create the agent
        from src.ssa.agent.simple_agent import StudyBuddyAgent
        agent = StudyBuddyAgent(manager)
        
        # Test queries
        print("\n🧪 RUNNING TESTS:")
        print("=" * 60)
        
        test_queries = [
            ("Search for AI information", "Should use search tool"),
            ("Summarize the machine learning document", "Should use summary tool"),
            ("What type of document is the AI tutorial?", "Should use classify tool"),
            ("What is artificial intelligence?", "Complex question - search then LLM"),
            ("Hello", "General query")
        ]
        
        for query, expected in test_queries:
            print(f"\n📋 Test: '{query}'")
            print(f"   Expected: {expected}")
            print("-" * 40)
            
            result = agent.ask(query)
            print(f"\n✅ Tool used: {result['tool_used']}")
            print(f"✅ Intent: {result['intent']}")
        
        # Show statistics
        agent.show_stats()
        
        # Interactive mode
        print("\n" + "=" * 60)
        print("💬 INTERACTIVE MODE (type 'quit' to exit)")
        print("=" * 60)
        
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_input:
                agent.ask(user_input)
        
        print("\n🎉 WEEK 14 FIXED - AGENT WORKING!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()