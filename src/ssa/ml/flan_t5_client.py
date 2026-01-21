# src/ssa/ml/flan_t5_client.py
from transformers import pipeline

class FlanT5Client:
    def __init__(self, model_size="small"):
        print(f"Loading Flan-T5-{model_size}...")
        self.generator = pipeline(
            "text2text-generation",
            model=f"google/flan-t5-{model_size}",
            device=-1,
            torch_dtype="auto"
        )
        print(f"✅ Flan-T5-{model_size} loaded")
    
    def generate(self, prompt, max_length=300, **kwargs):
        """
        Generate better responses with optimized parameters
        """
        # Better prompt formatting
        formatted_prompt = self._improve_prompt(prompt)
        
        # Optimized generation parameters for Flan-T5
        result = self.generator(
            formatted_prompt,
            max_new_tokens=max_length,  # Use max_new_tokens, not max_length
            temperature=0.8,            # More creative (0.7-0.9)
            do_sample=True,             # Enable sampling
            top_p=0.95,                 # Nucleus sampling
            repetition_penalty=1.1,     # Reduce repetition
            num_beams=2,                # Beam search for better quality
            early_stopping=True,        # Stop when good enough
            **kwargs
        )
        
        response = result[0]['generated_text'].strip()
        return self._clean_response(response)
    
    def _improve_prompt(self, prompt):
        """
        Drastically improve prompts for Flan-T5
        """
        prompt_lower = prompt.lower()
        
        # For questions
        if "?" in prompt:
            if any(word in prompt_lower for word in ["what is", "what are", "what does"]):
                return f"Define and explain: {prompt}"
            elif any(word in prompt_lower for word in ["how", "why"]):
                return f"Explain step by step: {prompt}"
            else:
                return f"Answer in detail: {prompt}"
        
        # For explanations
        elif any(word in prompt_lower for word in ["explain", "describe", "tell me about"]):
            return f"Provide a detailed explanation: {prompt}"
        
        # For summaries
        elif "summar" in prompt_lower:
            return prompt
        
        # Default
        return f"Respond to: {prompt}"
    
    def _clean_response(self, response):
        """Clean and improve response"""
        # Remove prompt if repeated
        lines = response.split('. ')
        if len(lines) > 1:
            # Take only the meaningful parts
            cleaned = []
            for line in lines:
                if len(line) > 10 and not line.startswith(("The", "A", "An", "In", "For")):
                    cleaned.append(line)
            if cleaned:
                return '. '.join(cleaned[:3]) + '.'
        
        return response
    
    def generate_better(self, prompt_type, content, **kwargs):
        """
        Specialized generation methods
        """
        if prompt_type == "qa":
            prompt = f"Provide a comprehensive answer: {content}"
        elif prompt_type == "explain":
            prompt = f"Explain in detail with examples: {content}"
        elif prompt_type == "summarize":
            prompt = f"Summarize key points: {content}"
        else:
            prompt = content
        
        return self.generate(prompt, **kwargs)