from src.ssa.core.manager import DocumentManager


manager = DocumentManager("data/documents.json")
X,Y = manager.prepare_difficlulty_training_data()


print("Feature vector example:", X[0])
print("Label example:", Y[0])