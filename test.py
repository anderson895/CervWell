import joblib

def load_file(filename):
    try:
        return joblib.load(filename)
    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")
        return None

# Load model, scaler, and features
model = load_file("cervical_cancer_model.pkl")
scaler = load_file("scaler.pkl")
feature_names = load_file("feature_names.pkl")
