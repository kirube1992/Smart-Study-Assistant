import re
from typing import List, Tuple
from collections import Counter


class AnswerExtractor:
    def __init__(self, min_sentence_length: int = 10, max_sentence_length: int = 200):
        self.min_sentence_length = min_sentence_length
        self.max_sentence_length = max_sentence_length

    def split_into_sentences(self, text: str) -> List[str]:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        clean = []

        for s in sentences:
            s = s.strip()
            if (
                self.min_sentence_length <= len(s) <= self.max_sentence_length
                and not s.lower().startswith(("figure", "table", "chapter", "section"))
            ):
                clean.append(s)

        return clean

    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        stopwords = {
            'the','a','an','and','or','in','on','at','to','for','of','with','is','are',
            'was','were','be','been','this','that','which','what','how','why','when'
        }

        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        filtered = [w for w in words if w not in stopwords]

        counts = Counter(filtered)
        return [w for w, _ in counts.most_common(top_n)]

    def score_sentence_relevance(self, question: str, sentence: str) -> float:
        q_keywords = self.extract_keywords(question)

        if not q_keywords:
            return 0.0

        sentence_lower = sentence.lower()
        matches = sum(1 for kw in q_keywords if kw in sentence_lower)

        return matches / len(q_keywords)

    def extract_answers(
        self,
        question: str,
        documents: List[Tuple],
        max_answers: int = 3,
        min_score: float = 0.2
    ) -> List[Tuple[str, float, str]]:

        all_answers = []

        for doc, doc_score in documents:
            sentences = self.split_into_sentences(doc.content)

            for sentence in sentences:
                s_score = self.score_sentence_relevance(question, sentence)
                combined = s_score * (0.5 + 0.5 * doc_score)

                if combined >= min_score:
                    all_answers.append((sentence, combined, doc.title))

        all_answers.sort(key=lambda x: x[1], reverse=True)
        return all_answers[:max_answers]
