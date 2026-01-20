#!/usr/bin/env python3
"""
Quick test script for Flan-T5
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🧪 Testing Flan-T5 Installation...")
print("=" * 50)

try:
    # Test 1: Import transformers
    print("1. Testing transformers import...")
    from transformers import pipeline
    print("   ✅ transformers imported")
    
    # Test 2: Load small model
    print("\n2. Loading Flan-T5-small (fastest)...")
    generator = pipeline("text2text-generation", model="google/flan-t5-small")
    print("   ✅ Model loaded")
    
    # Test 3: Generate response
    print("\n3. Testing generation...")
    result = generator("What is AI?", max_length=50)
    print(f"   Prompt: What is AI?")
    print(f"   Response: {result[0]['generated_text']}")
    
    # Test 4: Memory info
    print("\n4. System check...")
    import psutil
    memory = psutil.virtual_memory()
    print(f"   Available RAM: {memory.available / 1024**3:.1f} GB")
    print(f"   Used RAM: {memory.used / 1024**3:.1f} GB")
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("=" * 50)
    print("\n🎉 Flan-T5 is ready for Smart Study Assistant!")
    print("\nNext: Run 'python scripts/test_llm_qa.py' to test integration")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\n💡 Solution: pip install transformers torch")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Try these fixes:")
    print("1. Update pip: python -m pip install --upgrade pip")
    print("2. Install with: pip install transformers torch --no-cache-dir")
    print("3. If memory error, use smaller model: flan-t5-small")