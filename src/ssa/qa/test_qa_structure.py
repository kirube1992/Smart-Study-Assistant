from src.ssa.core.manager import DocumentManager
from src.ssa.qa.retriever import QARetriever
from src.ssa.qa.answer_extractor import AnswerExtractor


def run_week_11_test():
    print("\n=== WEEK 11: SIMPLE Q&A TEST ===\n")

    # 1️⃣ Load documents
    manager = DocumentManager("data/documents.json")

    # 2️⃣ Ensure embeddings exist
    manager.init_embedder(embedder_type="transformer")


    # 3️⃣ Initialize QA components
    retriever = QARetriever(manager)
    # pass the manager's embedder into the extractor so it can compute embeddings
    extractor = AnswerExtractor(manager.embedder)



    # 4️⃣ Ask a question
    question = "What is Machine learning"

    print(f"Question: {question}\n")

    # 5️⃣ Retrieve top documents
    retrieved = retriever.retrieve_for_question(question, top_k=3)
    documents = retriever.get_retrieved_documents(retrieved)

    print("Retrieved documents:")
    for doc, score in documents:
        print(f"- {doc.title} (score={score:.2f})")

    # 6️⃣ Extract answers
    answers = extractor.extract_answers(question, documents)

    print("\nAnswers:")
    print(extractor.format_answers(answers))


if __name__ == "__main__":
    run_week_11_test()

