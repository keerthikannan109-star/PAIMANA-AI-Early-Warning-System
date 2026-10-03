import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
INPUT_FILE = Path("data/processed/paimana_cleaned.csv")
OUTPUT_FILE = Path("data/processed/paimana_features.csv")

# -----------------------------
# Load cleaned data
# -----------------------------
df = pd.read_csv(INPUT_FILE)

# Convert dates again after CSV loading
df["original_end_date"] = pd.to_datetime(
    df["original_end_date"],
    errors="coerce"
)

df["revised_end_date"] = pd.to_datetime(
    df["revised_end_date"],
    errors="coerce"
)

# -----------------------------
# 1. Cost Overrun %
# -----------------------------
df["cost_overrun_pct"] = 0.0

valid_cost = df["original_cost_cr"] > 0

df.loc[valid_cost, "cost_overrun_pct"] = (
    (
        df.loc[valid_cost, "revised_cost_cr"]
        - df.loc[valid_cost, "original_cost_cr"]
    )
    / df.loc[valid_cost, "original_cost_cr"]
) * 100

# -----------------------------
# 2. Cost Overrun Flag
# -----------------------------
df["cost_overrun_flag"] = (
    df["cost_overrun_pct"] > 0
).astype(int)

# -----------------------------
# 3. Expenditure Ratio %
# -----------------------------
df["expenditure_ratio_pct"] = 0.0

valid_revised = df["revised_cost_cr"] > 0

df.loc[valid_revised, "expenditure_ratio_pct"] = (
    df.loc[valid_revised, "expenditure_cr"]
    / df.loc[valid_revised, "revised_cost_cr"]
) * 100

# -----------------------------
# 4. Schedule Delay Days
# -----------------------------
df["schedule_delay_days"] = 0.0

valid_dates = (
    df["original_end_date"].notna()
    & df["revised_end_date"].notna()
)

df.loc[valid_dates, "schedule_delay_days"] = (
    df.loc[valid_dates, "revised_end_date"]
    - df.loc[valid_dates, "original_end_date"]
).dt.days

# -----------------------------
# 5. Time Overrun Flag
# -----------------------------
df["time_overrun_flag"] = (
    df["schedule_delay_days"] > 0
).astype(int)

# -----------------------------
# 6. Absolute Cost Increase
# -----------------------------
df["cost_increase_cr"] = (
    df["revised_cost_cr"]
    - df["original_cost_cr"]
)

# -----------------------------
# 7. High Expenditure Flag
# -----------------------------
df["high_expenditure_flag"] = (
    df["expenditure_ratio_pct"] > 80
).astype(int)

# -----------------------------
# 8. Overall Risk Score
# -----------------------------
df["risk_score"] = (
    (df["cost_overrun_flag"] * 35)
    + (df["time_overrun_flag"] * 35)
    + (df["high_expenditure_flag"] * 30)
)

# -----------------------------
# 9. Risk Level
# -----------------------------
def get_risk_level(score):
    if score >= 80:
        return "Critical"
    elif score >= 50:
        return "High"
    elif score >= 30:
        return "Medium"
    else:
        return "Low"


df["risk_level"] = df["risk_score"].apply(get_risk_level)

# -----------------------------
# Save feature dataset
# -----------------------------
OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# -----------------------------
# Results
# -----------------------------
print("Feature engineering completed!")
print("Final shape:", df.shape)

print("\nNew features:")
print([
    "cost_overrun_pct",
    "cost_overrun_flag",
    "expenditure_ratio_pct",
    "schedule_delay_days",
    "time_overrun_flag",
    "cost_increase_cr",
    "high_expenditure_flag",
    "risk_score",
    "risk_level"
])

print("\nRisk distribution:")
print(df["risk_level"].value_counts())

print("\nSaved to:")
print(OUTPUT_FILE)