"""
Optimized Flan-T5 Client for Smart Study Assistant
"""

import time
from typing import List, Optional
from transformers import pipeline, AutoTokenizer
import logging

logger = logging.getLogger(__name__)


class FlanT5Client:
    """Flan-T5 Client with proper prompt formatting"""
    
    def __init__(self, model_size: str = "small"):
        self.model_size = model_size
        self.model_name = f"google/flan-t5-{model_size}"
        
        print(f"📥 Loading Flan-T5-{model_size}...")
        
        # Load with proper settings for Flan-T5
        self.generator = pipeline(
            "text2text-generation",
            model=self.model_name,
            device=-1,  # CPU
            torch_dtype="auto"
        )
        
        # Load tokenizer separately for better control
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        print(f"✅ Flan-T5-{model_size} ready! Max length: {self.tokenizer.model_max_length} tokens")
    
    def _format_prompt(self, prompt: str) -> str:
        """Format prompt for Flan-T5 model"""
        # Flan-T5 works best with explicit Q&A format
        if "?" in prompt and not prompt.strip().endswith(":"):
            # Check if it looks like a question
            question_words = ["what", "how", "why", "when", "where", "who", "explain", "describe"]
            if any(prompt.lower().startswith(word) for word in question_words):
                return f"Question: {prompt} Answer:"
        
        # For explanation/instruction prompts
        if "explain" in prompt.lower() or "describe" in prompt.lower():
            return f"Instruction: {prompt} Response:"
        
        return prompt
    
    def generate(
        self,
        prompt: str,
        max_length: int = 300,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate response with proper Flan-T5 formatting
        """
        # Format the prompt for Flan-T5
        formatted_prompt = self._format_prompt(prompt)
        
        try:
            # Generate with Flan-T5 optimized settings
            result = self.generator(
                formatted_prompt,
                max_length=max_length,
                temperature=temperature,
                do_sample=True if temperature > 0 else False,
                repetition_penalty=1.2,  # Reduce repetition
                num_beams=1,  # Greedy search for speed
                **kwargs
            )
            
            response = result[0]['generated_text'].strip()
            
            # Clean up the response
            if response.startswith("Answer:"):
                response = response[7:].strip()
            elif response.startswith("Response:"):
                response = response[9:].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"[LLM Error] Unable to generate response"
    
    def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        """Generate multiple responses"""
        formatted_prompts = [self._format_prompt(p) for p in prompts]
        try:
            results = self.generator(formatted_prompts, **kwargs)
            return [r['generated_text'].strip() for r in results]
        except Exception as e:
            logger.error(f"Batch generation error: {e}")
            return [f"[Error] {str(e)}"] * len(prompts)
    
    def test_generation(self):
        """Test the model with various prompts"""
        test_cases = [
            ("What is artificial intelligence?", "AI is the simulation of human intelligence by machines."),
            ("Explain neural networks:", "Neural networks are computing systems inspired by biological brains."),
            ("How does machine learning work?", "ML algorithms learn patterns from data to make predictions."),
        ]
        
        print("\n🧪 Testing Flan-T5 generation...")
        for prompt, expected_start in test_cases:
            print(f"\n📝 Prompt: {prompt}")
            response = self.generate(prompt, max_length=100, temperature=0.3)
            print(f"🤖 Response: {response}")
            
            if len(response) > 10:
                print("✅ Good response!")
            else:
                print("⚠️  Short response, might need better prompting")


# Quick test
if __name__ == "__main__":
    print("Testing Flan-T5 Client...")
    
    # Test with the already downloaded model
    client = FlanT5Client("small")
    
    # Test generation
    client.test_generation()
    
    # Test with your SSA-style prompts
    test_prompts = [
        "What is machine learning?",
        "Explain backpropagation in neural networks",
        "How do transformers work in NLP?"
    ]
    
    print("\n" + "=" * 50)
    print("SSA-Style Prompt Testing")
    print("=" * 50)
    
    for prompt in test_prompts:
        response = client.generate(prompt, max_length=150)
        print(f"\n❓ {prompt}")
        print(f"📝 {response[:100]}...")