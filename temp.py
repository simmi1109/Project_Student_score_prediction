from src.utils import load_object

print("Loading model...")
model = load_object("artifacts/model.pkl")
print("Model loaded")

print("Loading preprocessor...")
preprocessor = load_object("artifacts/preprocessor.pkl")
print("Preprocessor loaded")