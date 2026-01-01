from src.ssa.core.manager import DocumentManager

manager = DocumentManager("data/documents.json")

manager.train_difficulty_model()

test_text = """
Neural networks use backpropagation and gradient descent
to minimize loss functions across hidden layers.
"""

prediction = manager.predict_difficulty_ml(test_text)
print("Predicted difficulty:", prediction)
