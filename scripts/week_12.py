from src.ssa.ml.transformer_embedder import TransformerEmbedder

embedder = TransformerEmbedder()

v1 = embedder.encode("Machine learning is a field of AI.")
v2 = embedder.encode("Artificial intelligence systems learn from data.")

print(v1.shape)
print(embedder.similarity(v1, v2))
