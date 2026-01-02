class QAengine:
    def __init__(self, document_manager, embedder):
        self.document_manager = document_manager
        self.embedder = embedder

    def answer_question(self, question: str, top_k: int=3):
        pass