# src/ssa/ml/simple_llm.py
"""
Simple LLM that always works (DistilGPT2)
"""

from transformers import pipeline

class SimpleLLM:
    """DistilGPT2 - Small, fast, reliable"""
    
    def __init__(self):
        print("🚀 Loading DistilGPT2...")
        self.generator = pipeline("text-generation", model="distilgpt2")
        print("✅ DistilGPT2 ready!")
    
    def answer_question(self, question, max_length=150):
        """Simple Q&A"""
        result = self.generator(
            f"Q: {question}\nA:",
            max_length=max_length,
            temperature=0.7,
            do_sample=True,
            num_return_sequences=1
        )
        
        answer = result[0]['generated_text']
        # Extract answer part
        if "A:" in answer:
            return answer.split("A:")[-1].strip()
        return answer.replace(f"Q: {question}\nA:", "").strip()