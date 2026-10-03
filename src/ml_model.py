import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

# -----------------------------------
# Paths
# -----------------------------------
INPUT_FILE = Path("data/processed/paimana_features.csv")
MODEL_FILE = Path("models/risk_model.pkl")

# -----------------------------------
# Load dataset
# -----------------------------------
df = pd.read_csv(INPUT_FILE)

# -----------------------------------
# Features
# -----------------------------------
features = [
    "original_cost_cr",
    "revised_cost_cr",
    "expenditure_cr",
    "cost_overrun_pct",
    "expenditure_ratio_pct",
    "schedule_delay_days",
    "cost_increase_cr"
]

X = df[features]

# Target
y = df["risk_level"]

# -----------------------------------
# Train/Test Split
# -----------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# -----------------------------------
# Random Forest Model
# -----------------------------------
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_split=5,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# -----------------------------------
# Prediction
# -----------------------------------
y_pred = model.predict(X_test)

# -----------------------------------
# Metrics
# -----------------------------------
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)
recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)
f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    zero_division=0
))

# -----------------------------------
# Feature Importance
# -----------------------------------
importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
}).sort_values(
    "importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance.to_string(index=False))

# -----------------------------------
# Save model
# -----------------------------------
MODEL_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(model, MODEL_FILE)

print("\nModel saved to:")
print(MODEL_FILE)