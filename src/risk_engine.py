import pandas as pd
import joblib

from pathlib import Path


# ---------------------------------------
# Paths
# ---------------------------------------
DATA_FILE = Path("data/processed/paimana_cleaned.csv")

COST_MODEL = Path(
    "models/cost_overrun_xgboost.pkl"
)

TIME_MODEL = Path(
    "models/time_overrun_xgboost.pkl"
)


# ---------------------------------------
# Load models
# ---------------------------------------
cost_model = joblib.load(COST_MODEL)
time_model = joblib.load(TIME_MODEL)

df = pd.read_csv(DATA_FILE)


# ---------------------------------------
# Prepare data
# ---------------------------------------
features = [
    "original_cost_cr",
    "sector",
    "ministry"
]

X = df[features].copy()


# ---------------------------------------
# Prediction probabilities
# ---------------------------------------
cost_probability = cost_model.predict_proba(X)[:, 1]

time_probability = time_model.predict_proba(X)[:, 1]


# ---------------------------------------
# Risk Score
# ---------------------------------------
df["cost_risk_probability"] = cost_probability

df["time_risk_probability"] = time_probability

df["risk_score"] = (
    (cost_probability * 50) +
    (time_probability * 50)
)


# ---------------------------------------
# Risk Level
# ---------------------------------------
def get_risk_level(score):

    if score >= 75:
        return "Critical"

    elif score >= 50:
        return "High"

    elif score >= 25:
        return "Medium"

    else:
        return "Low"


df["risk_level"] = df["risk_score"].apply(
    get_risk_level
)


# ---------------------------------------
# Early Warning
# ---------------------------------------
def generate_warning(row):

    warnings = []

    if row["cost_risk_probability"] >= 0.60:
        warnings.append(
            "Cost Overrun Risk"
        )

    if row["time_risk_probability"] >= 0.60:
        warnings.append(
            "Time Overrun Risk"
        )

    if not warnings:
        return "No Immediate Warning"

    return " + ".join(warnings)


df["early_warning"] = df.apply(
    generate_warning,
    axis=1
)


# ---------------------------------------
# Save output
# ---------------------------------------
output_file = Path(
    "data/processed/project_risk_predictions.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ---------------------------------------
# Display summary
# ---------------------------------------
print("\n================================")
print("RISK ENGINE COMPLETED")
print("================================")

print(
    "\nRisk Level Distribution:"
)

print(
    df["risk_level"].value_counts()
)

print(
    "\nEarly Warning Distribution:"
)

print(
    df["early_warning"].value_counts()
)

print(
    "\nAverage Risk Score:",
    round(df["risk_score"].mean(), 2)
)

print(
    "\nSaved to:"
)

print(output_file)


# ---------------------------------------
# Show top 10 high-risk projects
# ---------------------------------------
print(
    "\nTop 10 High-Risk Projects:"
)

top_projects = df.sort_values(
    "risk_score",
    ascending=False
)[
    [
        "project_name",
        "sector",
        "risk_score",
        "risk_level",
        "early_warning"
    ]
].head(10)

print(
    top_projects.to_string(
        index=False
    )
)