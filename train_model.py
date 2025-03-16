import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, confusion_matrix

print("Training Random Forest Model...")

# Load dataset
df = pd.read_csv("risk_factors_cervical_cancer.csv")

# Replace '?' with NaN and convert to numeric
df.replace("?", np.nan, inplace=True)
df = df.apply(pd.to_numeric, errors='coerce')

# Fill missing values with median
df.fillna(df.median(), inplace=True)

# Define Features and Target
target_column = "Dx:Cancer"
drop_columns = ["Hinselmann", "Schiller", "Citology", "Biopsy", "Dx", target_column]
X = df.drop(columns=drop_columns)  # Select only relevant features
y = df[target_column]  

# ✅ Compute and Save Median Values
median_values = X.median().to_dict()
joblib.dump(median_values, "median_values.pkl")
print("✅ Median Values Saved Successfully!")

# Normalize using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save feature names to ensure correct input during prediction
feature_names = X.columns.tolist()
joblib.dump(feature_names, "feature_names.pkl")

# Apply SMOTE to balance classes
smote = SMOTE(sampling_strategy=0.3, random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, stratify=y_resampled, random_state=42)

# Train the Model
rf_model = RandomForestClassifier(n_estimators=300, max_depth=4, min_samples_split=10, random_state=42)
rf_model.fit(X_train, y_train)

# Save Model and Scaler
joblib.dump(rf_model, "cervical_cancer_model.pkl")
joblib.dump(scaler, "scaler.pkl")

# Predict using the model
y_pred_best = rf_model.predict(X_test)
y_pred_proba = rf_model.predict_proba(X_test)[:, 1]  # Probabilities for AUC-ROC

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred_best)
auc_roc = roc_auc_score(y_test, y_pred_proba)
conf_matrix = confusion_matrix(y_test, y_pred_best)
class_report = classification_report(y_test, y_pred_best)

# Print the results
print("Final Best Model Accuracy:", accuracy)
print("Final Best Model AUC-ROC Score:", auc_roc)
print("Final Best Model Confusion Matrix:\n", conf_matrix)
print("Final Best Model Classification Report:\n", class_report)

# Optionally, save the classification report to a text file
with open("classification_report.txt", "w") as file:
    file.write(class_report)

print("✅ Model, Scaler, and Medians Saved Successfully!")
print("✅ Classification Report Saved to classification_report.txt!")
