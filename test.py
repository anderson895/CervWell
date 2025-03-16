import os
import joblib
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load feature names and median values safely
try:
    if os.path.exists("feature_names.pkl"):
        feature_names = joblib.load("feature_names.pkl")
        logger.info("✅ feature_names.pkl loaded successfully!")
    else:
        raise FileNotFoundError("❌ feature_names.pkl not found!")

    if os.path.exists("median_values.pkl"):
        median_values = joblib.load("median_values.pkl")
        logger.info("✅ median_values.pkl loaded successfully!")
    else:
        raise FileNotFoundError("❌ median_values.pkl not found!")

except Exception as e:
    logger.error(f"❌ Error loading necessary files: {e}")
    feature_names = None
    median_values = None
