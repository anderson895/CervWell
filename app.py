import numpy as np
import joblib
import pandas as pd
import logging
from flask import Flask, request, jsonify, render_template

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load trained model, scaler, feature names, and median values
try:
    model = joblib.load("cervical_cancer_model.pkl")
    scaler = joblib.load("scaler.pkl")
    feature_names = joblib.load("feature_names.pkl")
    median_values = joblib.load("median_values.pkl")  # ✅ Load Median Values
    logger.info("✅ Model, Scaler, Features, and Medians Loaded Successfully!")
except Exception as e:
    logger.error(f"❌ Error Loading Model or Scaler: {e}")

@app.route("/")
def landing():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        logger.info("📥 Received Data: %s", data)

        # Function to safely convert values or use median values
        def safe_convert(value, key):
            try:
                return float(value)
            except (ValueError, TypeError):
                logger.warning(f"❌ Invalid value for {key}: {value}, using median: {median_values.get(key, 0)}")
                return median_values.get(key, 0)  # ✅ Use median if invalid

        # Validate & Convert Data
        corrected_data = {feature: safe_convert(data.get(feature), feature) for feature in feature_names}

        logger.info("🔍 Processed Input Data: %s", corrected_data)

        # Convert to DataFrame & Ensure Correct Order
        input_df = pd.DataFrame([corrected_data])
        logger.info("🛠 DataFrame Before Scaling:\n%s", input_df)

        # Scale Input Data
        input_scaled = scaler.transform(input_df)
        logger.info("📊 Scaled Input: %s", input_scaled)

        # Get Prediction & Probability
        prediction = model.predict(input_scaled)[0]
        probabilities = model.predict_proba(input_scaled)[0]

        logger.info("🔍 Probability Distribution: %s", probabilities)

        response = {
            "prediction": "High Risk" if prediction == 1 else "Low Risk",
            "probability": float(round(probabilities[1] * 100, 2)),
            "full_probabilities": probabilities.tolist()
        }

        logger.info("📤 Response Sent: %s", response)
        return jsonify(response)

    except Exception as e:
        logger.error("❌ Error: %s", str(e))
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)
