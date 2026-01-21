# scripts/test_phi2_direct_transformers.py
"""
Direct Phi-2 test without custom class
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("🧪 Direct Phi-2 Test (No custom class)")
print("=" * 50)

try:
    from transformers import pipeline
    
    print("🚀 Loading Phi-2 with pipeline...")
    
    # Use pipeline for simplicity
    generator = pipeline(
        "text-generation",
        model="microsoft/phi-2",
        device_map="auto",
        torch_dtype="auto",
        trust_remote_code=True
    )
    
    print("✅ Phi-2 pipeline ready!")
    
    # Test with short prompt
    questions = [
        "What is artificial intelligence?",
        "What is machine learning?"
    ]
    
    for q in questions:
        print(f"\n❓ {q}")
        
        # Very short generation first
        result = generator(
            f"Q: {q}\nA:",
            max_length=100,  # Very short
            temperature=0.7,
            do_sample=True,
            num_return_sequences=1
        )
        
        answer = result[0]['generated_text']
        # Extract answer part
        if "A:" in answer:
            answer = answer.split("A:")[-1].strip()
        
        print(f"🤖 {answer[:150]}...")
    
    print("\n✅ Phi-2 working with pipeline!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Try: pip install --upgrade transformers accelerate")

print("\n" + "=" * 50)