from src.ssa.core.manager import DocumentManager

manager = DocumentManager("data/documents.json")
manager.vectorize_documents()
manager.cluster_documents(n_clusters=3)
manager.show_clusters()

