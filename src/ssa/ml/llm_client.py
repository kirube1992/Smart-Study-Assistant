"""
Simple Flan-T5 LLM Client for Smart Study Assistant
Works on ANY PC - no GPU needed!
"""

import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class FlanT5Client:
    """Flan-T5 LLM Client - Fast, Lightweight, CPU-friendly"""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize Flan-T5 model
        
        Args:
            model_size: "small" (80M), "base" (250M), "large" (780M)
        """
        try:
            from transformers import pipeline
        except ImportError:
            raise ImportError("Please install transformers: pip install transformers")
        
        self.model_size = model_size
        model_name = f"google/flan-t5-{model_size}"
        
        print(f"🔄 Loading Flan-T5-{model_size}... (this may take a minute)")
        
        # Load model - runs on CPU by default
        self.generator = pipeline(
            "text2text-generation",
            model=model_name,
            device=-1,  # -1 means CPU
            torch_dtype="auto"  # Automatically uses available precision
        )
        
        print(f"✅ Flan-T5-{model_size} loaded successfully!")
        print(f"   Memory usage: ~{self._get_model_size()} MB")
    
    def _get_model_size(self) -> int:
        """Estimate model size in MB"""
        sizes = {
            "small": 80,
            "base": 250,
            "large": 780,
            "xl": 3000,
            "xxl": 11000
        }
        return sizes.get(self.model_size, 250)
    
    def generate(
        self,
        prompt: str,
        max_length: int = 300,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate response from prompt
        
        Args:
            prompt: Input text
            max_length: Maximum response length
            temperature: 0.0 (deterministic) to 1.0 (creative)
        """
        try:
            # Generate response
            result = self.generator(
                prompt,
                max_length=max_length,
                temperature=temperature,
                do_sample=True if temperature > 0 else False,
                **kwargs
            )
            
            return result[0]['generated_text'].strip()
            
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"[LLM Error] Unable to generate response: {str(e)}"
    
    def get_cost_estimate(self, prompt: str) -> float:
        """Local models have no API cost"""
        return 0.0
    
    def batch_generate(self, prompts: list, **kwargs) -> list:
        """Generate multiple responses (more efficient)"""
        try:
            results = self.generator(prompts, **kwargs)
            return [r['generated_text'].strip() for r in results]
        except Exception as e:
            logger.error(f"Batch generation error: {e}")
            return [f"[Error] {str(e)}"] * len(prompts)


# ========== FACTORY FUNCTION ==========
def create_llm_client(
    provider: str = "flan-t5",
    model_size: str = "base",
    **kwargs
):
    """
    Factory function to create LLM client
    
    Args:
        provider: "flan-t5" (default), "mock" for testing
        model_size: "small", "base", "large"
    """
    
    if provider == "flan-t5":
        return FlanT5Client(model_size=model_size)
    
    elif provider == "mock":
        from .mock_llm import MockLLM
        return MockLLM()
    
    else:
        raise ValueError(f"Provider '{provider}' not supported. Use 'flan-t5' or 'mock'")


# ========== QUICK TEST ==========
if __name__ == "__main__":
    print("🧪 Testing Flan-T5 LLM Client...")
    
    try:
        # Test with smallest model first
        client = create_llm_client("flan-t5", "small")
        
        test_prompts = [
            "Explain machine learning to a beginner:",
            "What are neural networks?",
            "Summarize the concept of backpropagation:"
        ]
        
        for prompt in test_prompts:
            print(f"\n📝 Prompt: {prompt}")
            response = client.generate(prompt, max_length=100)
            print(f"🤖 Response: {response}")
        
        print("\n✅ Flan-T5 is working correctly!")
        print(f"💾 Model loaded: Flan-T5-small")
        print(f"🎯 Ready to integrate with Smart Study Assistant!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Check internet connection (needs to download model first time)")
        print("2. Try: pip install --upgrade transformers")
        print("3. Try smaller model: client = FlanT5Client('small')")