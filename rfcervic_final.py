import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel

print("Training Random Forest Model")

# Load dataset
file_path = r"risk_factors_cervical_cancer.csv"
df = pd.read_csv(file_path)

# Data Cleaning
df.replace("?", np.nan, inplace=True)  
df = df.apply(pd.to_numeric, errors='coerce')  

# Impute missing values
for col in df.columns:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())  

# Feature Engineering 
df["Age_SexPartners"] = df["Age"] * df["Number of sexual partners"]  # Interaction feature
df["Log_Age"] = np.log(df["Age"] + 1)  # Log transformation to reduce skewness

# Define features and target
target_column = "Dx:Cancer"
X = df.drop(columns=[target_column])  
y = df[target_column]  

# Normalize data 
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# SMOTE
smote = SMOTE(sampling_strategy=0.3, random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

# 30% test set, 70% train set
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.3, stratify=y_resampled, random_state=42
)

# Hyperparameter tuning 
param_grid = {
    "n_estimators": [200, 300],  
    "max_depth": [3, 4],   
    "min_samples_split": [7, 10], 
}

# Random Forest Model
rf_temp = RandomForestClassifier(n_estimators=200, random_state=42)
rf_temp.fit(X_train, y_train)

# Feature Selection
selector = SelectFromModel(rf_temp, threshold="median", prefit=True)
X_train_selected = selector.transform(X_train)
X_test_selected = selector.transform(X_test)

# Model Training
grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring="accuracy", n_jobs=-1)
grid_search.fit(X_train_selected, y_train)

# Best Model
best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test_selected)

# Model Evaluation
print("Final Best Model Accuracy:", accuracy_score(y_test, y_pred_best))
print("Final Best Model AUC-ROC Score:", roc_auc_score(y_test, best_model.predict_proba(X_test_selected)[:, 1]))
print("Final Best Model Confusion Matrix:\n", confusion_matrix(y_test, y_pred_best))
print("Final Best Model Classification Report:\n", classification_report(y_test, y_pred_best))
