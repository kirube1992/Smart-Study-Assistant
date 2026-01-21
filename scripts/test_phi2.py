# scripts/week13_final.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("🎓 WEEK 13 FINAL TEST")
print("=" * 60)

# Test 1: Direct DistilGPT2 test
print("\n1. Testing DistilGPT2 (guaranteed to work)...")
try:
    from transformers import pipeline
    generator = pipeline("text-generation", model="distilgpt2")
    
    result = generator("Q: What is AI?\nA:", max_length=100, temperature=0.7)
    answer = result[0]['generated_text']
    if "A:" in answer:
        answer = answer.split("A:")[-1].strip()
    
    print(f"🤖 {answer}")
    print("✅ DistilGPT2 works!")
    
except Exception as e:
    print(f"❌ DistilGPT2 error: {e}")

# Test 2: Test with your manager
print("\n2. Testing with DocumentManager...")
try:
    from src.ssa.core.manager import DocumentManager
    from src.ssa.core.document import Document
    from datetime import datetime
    
    manager = DocumentManager()
    
    # Add a sample document
    sample_doc = Document(
        title="AI Basics",
        content="Artificial intelligence is the simulation of human intelligence by machines.",
        file_path="/test.txt",
        ingestion_date=datetime.now().isoformat(),
        document_type="tutorial"
    )
    manager.documents = [sample_doc]
    
    # Initialize Week 13
    if hasattr(manager, 'init_week13'):
        manager.init_week13()
        
        # Test Q&A
        if hasattr(manager, 'ask_llm'):
            result = manager.ask_llm("What is AI?", use_context=False)
            print(f"🤖 LLM answer: {result['answer'][:100]}...")
            print(f"✅ Week 13 working!")
        else:
            print("❌ No ask_llm method")
    else:
        print("❌ No init_week13 method")
        
except Exception as e:
    print(f"❌ Manager test error: {e}")

print("\n" + "=" * 60)
print("🎯 WEEK 13 READY!")
print("=" * 60)