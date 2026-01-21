# src/ssa/ml/phi2_client.py - UPDATED
"""
Phi-2 Client with CPU optimizations
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class Phi2Client:
    def __init__(self, use_cpu=True):
        print("🚀 Loading Phi-2...")
        
        self.model_name = "microsoft/phi-2"
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, 
            trust_remote_code=True,
            padding_side="left"  # Important for Phi-2
        )
        
        # Set pad token if missing
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model with CPU optimization
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32 if use_cpu else torch.float16,  # Use float32 for CPU
            device_map="cpu" if use_cpu else "auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True  # Critical for CPU
        )
        
        # Move to eval mode
        self.model.eval()
        print("✅ Phi-2 loaded (CPU optimized)")
    
    def generate(self, prompt, max_tokens=100):
        """Generate response with CPU optimizations"""
        try:
            # Tokenize
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                padding=True,
                truncation=True,
                max_length=512
            )
            
            # Generate with strict limits for CPU
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=inputs.input_ids,
                    attention_mask=inputs.attention_mask,
                    max_new_tokens=max_tokens,  # Use max_new_tokens, not max_length
                    temperature=0.7,
                    do_sample=True,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=3,
                    early_stopping=True  # Stop early if possible
                )
            
            # Decode
            text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove prompt
            if text.startswith(prompt):
                text = text[len(prompt):].strip()
            
            return text
            
        except Exception as e:
            print(f"⚠️  Generation error: {e}")
            return f"[Error: {str(e)[:50]}]"
    
    def answer_question(self, question):
        """Simple Q&A"""
        prompt = f"Question: {question}\nAnswer:"
        return self.generate(prompt, max_tokens=80)  # Very short for CPU