import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)
from xgboost import XGBClassifier


INPUT_FILE = Path("data/processed/paimana_cleaned.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_FILE)

df["original_end_date"] = pd.to_datetime(
    df["original_end_date"],
    errors="coerce"
)

# Features available before the final outcome
features = [
    "original_cost_cr",
    "sector",
    "ministry"
]

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
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


def evaluate_model(name, model, X_test, y_test):

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )
    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )
    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    print(f"\n{name}")
    print("-" * 35)
    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    return accuracy, precision, recall, f1


# =====================================================
# COST OVERRUN — XGBOOST
# =====================================================

print("\n================================")
print("XGBOOST COST OVERRUN MODEL")
print("================================")

cost_df = df[
    (df["original_cost_cr"] > 0) &
    (df["revised_cost_cr"] > 0)
].copy()

cost_df["cost_overrun"] = (
    cost_df["revised_cost_cr"] >
    cost_df["original_cost_cr"]
).astype(int)

X = cost_df[features]
y = cost_df["cost_overrun"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

cost_xgb = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            XGBClassifier(
                n_estimators=300,
                max_depth=4,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                objective="binary:logistic",
                eval_metric="logloss",
                random_state=42
            )
        )
    ]
)

cost_xgb.fit(X_train, y_train)

cost_metrics = evaluate_model(
    "Cost Overrun - XGBoost",
    cost_xgb,
    X_test,
    y_test
)

joblib.dump(
    cost_xgb,
    MODEL_DIR / "cost_overrun_xgboost.pkl"
)

print(
    "\nSaved:",
    MODEL_DIR / "cost_overrun_xgboost.pkl"
)


# =====================================================
# TIME OVERRUN — XGBOOST
# =====================================================

print("\n================================")
print("XGBOOST TIME OVERRUN MODEL")
print("================================")

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

time_df["time_overrun"] = (
    time_df["revised_end_date"] >
    time_df["original_end_date"]
).astype(int)

X = time_df[features]
y = time_df["time_overrun"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

time_xgb = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            XGBClassifier(
                n_estimators=300,
                max_depth=4,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                objective="binary:logistic",
                eval_metric="logloss",
                random_state=42
            )
        )
    ]
)

time_xgb.fit(X_train, y_train)

time_metrics = evaluate_model(
    "Time Overrun - XGBoost",
    time_xgb,
    X_test,
    y_test
)

joblib.dump(
    time_xgb,
    MODEL_DIR / "time_overrun_xgboost.pkl"
)

print(
    "\nSaved:",
    MODEL_DIR / "time_overrun_xgboost.pkl"
)


# =====================================================
# FINAL SUMMARY
# =====================================================

print("\n========================================")
print("XGBOOST TRAINING COMPLETED")
print("========================================")

print(
    f"\nCost Overrun F1 : {cost_metrics[3]:.4f}"
)

print(
    f"Time Overrun F1 : {time_metrics[3]:.4f}"
)