import re
from typing import List, Tuple
from collections import Counter


class AnswerExtractor:
    def __init__(self,embedder, min_sentence_length: int = 10, max_sentence_length: int = 200):
        self.min_sentence_length = min_sentence_length
        self.max_sentence_length = max_sentence_length
        self.embedder = embedder
    def embed_sentences(self, sentences):
        return self.embedder.embed_batch(sentences)

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

    def score_sentence_relevance(self, question_embedding, sentence_embedding):
        return self.embedder.similarity(
            question_embedding,
            sentence_embedding
        )
        

    def extract_answers(
        self,
        question,
        documents,
        max_answers= 3,
        min_score = 0.3,
        ):

        all_answers = []

        question_embedding = self.embedder.embed_batch([question])[0]


        for doc, doc_score in documents:
            sentences = self.split_into_sentences(doc.content)
            if not sentences:
                continue

            sentence_embeddings = self.embedder.embed_batch(sentences)



            for sentence, sent_emb in zip(sentences, sentence_embeddings):
                sim = self.score_sentence_relevance(
                    question_embedding,
                    sent_emb)

                combined = sim * (0.5 + 0.5 * doc_score)
                
                if combined >= min_score:
                    all_answers.append(
                    (sentence, combined,doc.title)
                    )
        # sort and return top answers after processing all documents
        all_answers.sort(key=lambda x: x[1], reverse=True)
        return all_answers[:max_answers]
    def format_answers(self, answers: List[Tuple[str, float, str]]) -> str:
        if not answers:
            return "I couldn't find a clear answer in your study materials."

        formatted = []
        for i, (answer, score, source) in enumerate(answers, 1):
            confidence = "" if score > 0.5 else "~"
            formatted.append(
                f"{i}. {answer}\n   Source: {source} {confidence}"
            )

        return "\n\n".join(formatted)
    def explain_sentence(
            self,
            question:str,
            sentence:str,
            doc_score:float
    ) ->dict:
        keywords = self.extract_keywords(question)
        sentence_lower = sentence.lower()

        matched = [kw for kw in keywords if kw in sentence_lower]
        sentence_score = self.score_sentence_relevance(question, sentence)

        combined_score = self.score_sentence_relevance(question, sentence)

        return {
            "sentence":sentence,
            "matched_keywords":matched,
            "sentence_score":round(sentence_score,3),
            "document_score":round(doc_score,3),
            "combined_score": round(combined_score,3),
        }

