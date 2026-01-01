import re
import numpy as np
from datetime import datetime

class Document:
    def __init__(self, title, content, file_path, ingestion_date, document_type):
        self.title = title
        self.content = content
        self.file_path = file_path
        self.ingestion_date = ingestion_date
        self.tokens = []
        self.document_type = document_type
        self.difficulty_score = 0
        self.difficulty_label = None
        self.cluster_id = None
    def preprocess_text(self):
        text_lower = self.content.lower()
        text = re.sub(r'[^\w\s]', '', text_lower)
        self.tokens = text.split()
        return self.tokens
    def tokens_to_numeric(self):
        if not self.tokens:
            self.preprocess_text()
        self.numeric_token = np.array([len(word) for word in self.tokens])
        return self.numeric_token
    def calculate_difficulty(self):
        if not self.tokens:
            self.preprocess_text()

        word_count = len(self.tokens)
        if word_count == 0:
            self.difficulty_label = "easy"
            return self.difficulty_label
        
        ave_word_length = sum(len(w) for w in self.tokens)/word_count
        unique_ratio = len(set(self.tokens))/word_count
        long_word_ratio = len([w for w in self.tokens if len(w) > 6])/word_count

        self.difficulty_score = (
            ave_word_length * 0.4 + 
            unique_ratio * 8 +
            long_word_ratio * 15 +
            word_count * 0.01
        )

        if self.difficulty_score < 3:
            self.difficulty_label = "easy"
        elif self.difficulty_score < 11:
            self.difficulty_label = "medium"
        else:
            self.difficulty_label = "hard"
        return self.difficulty_label
    def __str__(self):
        return f"Document title: {self.title}, document filePath: {self.file_path}, date of ingestion: {self.ingestion_date}"
    def __repr__(self):
        return f"{self.title} {self.file_path} {self.ingestion_date}"
    def to_dict(self):
        """Convert document to dictionary for JSON serialization."""
        return {
            "title": self.title,
            "content": self.content,
            "file_path": self.file_path,
            "ingestion_date": self.ingestion_date,
            "document_type": self.document_type
        }

    @classmethod
    def from_dict(cls, data):
        """Create document from dictionary."""
        return cls(
            title=data.get("title", ""),
            content=data.get("content", ""),
            file_path=data.get("file_path", ""),
            ingestion_date=data.get("ingestion_date"),
            document_type=data.get("document_type")
        )
    