import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

# ---------------------------------------
# Paths
# ---------------------------------------
INPUT_FILE = Path("data/processed/paimana_cleaned.csv")
MODEL_DIR = Path("models")

MODEL_DIR.mkdir(exist_ok=True)

# ---------------------------------------
# Load data
# ---------------------------------------
df = pd.read_csv(INPUT_FILE)

df["original_end_date"] = pd.to_datetime(
    df["original_end_date"],
    errors="coerce"
)

print("Dataset shape:", df.shape)

# =======================================
# COST OVERRUN MODEL
# =======================================

# Only projects having valid original + revised cost
cost_df = df[
    (df["original_cost_cr"] > 0) &
    (df["revised_cost_cr"] > 0)
].copy()

# Target: revised cost greater than original cost
cost_df["cost_overrun"] = (
    cost_df["revised_cost_cr"] >
    cost_df["original_cost_cr"]
).astype(int)

print("\n==============================")
print("COST OVERRUN MODEL")
print("==============================")

print("Valid projects:", len(cost_df))
print("No cost overrun:", (cost_df["cost_overrun"] == 0).sum())
print("Cost overrun:", (cost_df["cost_overrun"] == 1).sum())

# ---------------------------------------
# Leakage-free input features
# ---------------------------------------
cost_features = [
    "original_cost_cr",
    "sector",
    "ministry"
]

X = cost_df[cost_features]
y = cost_df["cost_overrun"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

categorical_features = [
    "sector",
    "ministry"
]

numeric_features = [
    "original_cost_cr"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)

cost_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                class_weight="balanced"
            )
        )
    ]
)

cost_model.fit(X_train, y_train)

cost_pred = cost_model.predict(X_test)

print("\nCost Overrun Performance")
print("------------------------------")

print(
    f"Accuracy  : "
    f"{accuracy_score(y_test, cost_pred):.4f}"
)

print(
    f"Precision : "
    f"{precision_score(y_test, cost_pred, zero_division=0):.4f}"
)

print(
    f"Recall    : "
    f"{recall_score(y_test, cost_pred, zero_division=0):.4f}"
)

print(
    f"F1 Score  : "
    f"{f1_score(y_test, cost_pred, zero_division=0):.4f}"
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        cost_pred,
        zero_division=0
    )
)

joblib.dump(
    cost_model,
    MODEL_DIR / "cost_overrun_model.pkl"
)

print(
    "\nSaved:",
    MODEL_DIR / "cost_overrun_model.pkl"
)


# =======================================
# TIME OVERRUN MODEL
# =======================================

time_df = df[
    df["original_end_date"].notna() &
    df["revised_end_date"].notna()
].copy()

time_df["revised_end_date"] = pd.to_datetime(
    time_df["revised_end_date"],
    errors="coerce"
)

time_df = time_df[
    time_df["revised_end_date"].notna()
].copy()

# Target
time_df["time_overrun"] = (
    time_df["revised_end_date"] >
    time_df["original_end_date"]
).astype(int)

print("\n==============================")
print("TIME OVERRUN MODEL")
print("==============================")

print("Valid projects:", len(time_df))
print(
    "No time overrun:",
    (time_df["time_overrun"] == 0).sum()
)
print(
    "Time overrun:",
    (time_df["time_overrun"] == 1).sum()
)

# ---------------------------------------
# Leakage-free features
# ---------------------------------------
time_features = [
    "original_cost_cr",
    "sector",
    "ministry"
]

X = time_df[time_features]
y = time_df["time_overrun"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

time_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                class_weight="balanced"
            )
        )
    ]
)

time_model.fit(X_train, y_train)

time_pred = time_model.predict(X_test)

print("\nTime Overrun Performance")
print("------------------------------")

print(
    f"Accuracy  : "
    f"{accuracy_score(y_test, time_pred):.4f}"
)

print(
    f"Precision : "
    f"{precision_score(y_test, time_pred, zero_division=0):.4f}"
)

print(
    f"Recall    : "
    f"{recall_score(y_test, time_pred, zero_division=0):.4f}"
)

print(
    f"F1 Score  : "
    f"{f1_score(y_test, time_pred, zero_division=0):.4f}"
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        time_pred,
        zero_division=0
    )
)

joblib.dump(
    time_model,
    MODEL_DIR / "time_overrun_model.pkl"
)

print(
    "\nSaved:",
    MODEL_DIR / "time_overrun_model.pkl"
)

print("\n================================")
print("BOTH MODELS TRAINED SUCCESSFULLY")
print("================================")