# scripts/week13_integration_test.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("🎓 WEEK 13 INTEGRATION TEST")
print("=" * 60)

# Test 1: Direct DistilGPT2 with better parameters
print("\n1. Testing DistilGPT2 (improved)...")
from transformers import pipeline

generator = pipeline("text-generation", model="distilgpt2")

test_result = generator(
    "Question: What is artificial intelligence?\nAnswer:",
    max_new_tokens=80,
    temperature=0.8,
    repetition_penalty=1.2,
    truncation=True
)

answer = test_result[0]['generated_text']
if "Answer:" in answer:
    answer = answer.split("Answer:")[-1].strip()

print(f"🤖 {answer}")
print("✅ DistilGPT2 works with better parameters!")

# Test 2: Test your manager
print("\n2. Testing DocumentManager integration...")
try:
    from src.ssa.core.manager import DocumentManager
    
    manager = DocumentManager()
    
    # Check if method exists
    if hasattr(manager, 'init_week13'):
        print("✅ init_week13 method exists")
        
        # Initialize
        success = manager.init_week13()
        if success and hasattr(manager, 'ask_gpt2'):
            print("✅ LLM initialized")
            
            # Test Q&A
            result = manager.ask_gpt2("What is machine learning?")
            print(f"🤖 Answer: {result['answer'][:100]}...")
            print(f"📊 Model: {result.get('model', 'unknown')}")
            print(f"📅 Week: {result.get('week', 'unknown')}")
            
            print("\n✅ WEEK 13 INTEGRATION SUCCESSFUL!")
        else:
            print("❌ LLM initialization failed")
    else:
        print("❌ init_week13 method not found in manager")
        print("💡 Add the methods shown above to your manager.py")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("🎯 NEXT STEPS:")
print("1. Add init_week13() and ask_gpt2() methods to manager.py")
print("2. Run this test again")
print("3. Week 13 is complete!")
print("=" * 60)