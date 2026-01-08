import numpy as np
from typing import List, Dict, Any
import warnings
warnings.filterwarnings('ignore')


class trasformerEmbedder:
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        
        self.model = None
        self.model_name = None
        self.vector_size =None
        self.loaded = False
        self.load_falied = False

        self.model_dims = {
            "all-MiniLM-L6-v2": 384,
            "all-mpnet-base-v2": 768,
            "paraphrase-MiniLM-L3-v2": 384
        }