from typing import Optional, List, Dict, Any
import warnings
warnings.filterwarnings("ignore")
from transformers import pipeline
import numpy 

class DocumentSummarizer:

    def __init__(
            self,
            model_name: str = "sshleifer/distilbart-cnn-12-6",
            max_length: int = 130,
            min_length: int = 40,
    ):
        self.model_name = model_name
        self.max_length = max_length
        self.min_length = min_length
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            print(f"Loading: {self.model_name}")
            self._pipeline = pipeline(
                "summarization",
                model=self.model_name
            )
        return self._pipeline
        
    def summarize(self, text: str) -> Optional[str]:
        if not text:
            return None
        
        word_count = len(text.strip().split())
        if word_count < 20:
            return text.strip()
        elif word_count < 50:
            result = self.pipeline(
                text,
                max_length=min(self.max_length, word_count // 2),
                min_length=min(self.min_length, word_count // 3),
                do_sample=False,    
                truncation=True
            )
            return result[0]["summary_text"]
        else:
            result = self.pipeline(   
                text,
                max_length=self.max_length,
                min_length=self.min_length,
                do_sample=False, 
                truncation=True        
            )
            return result[0]["summary_text"]  
    
    def summarize_document(self, document) -> Optional[str]:
        if hasattr(document, 'content'):
            return self.summarize(document.content)
        return self.summarize(str(document))