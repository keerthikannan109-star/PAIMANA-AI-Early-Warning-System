import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
INPUT_FILE = Path("data/raw/Projects_Report.csv")
OUTPUT_FILE = Path("data/processed/paimana_cleaned.csv")

# -----------------------------
# Load PAIMANA dataset
# -----------------------------
df = pd.read_csv(INPUT_FILE, skiprows=2)

print("Original shape:", df.shape)

# -----------------------------
# Clean column names
# -----------------------------
df.columns = [
    "sr_no",
    "sector",
    "ministry",
    "project_code",
    "project_name",
    "original_cost_cr",
    "revised_cost_cr",
    "expenditure_cr",
    "original_end_date",
    "revised_end_date",
]

# -----------------------------
# Clean numeric columns
# -----------------------------
numeric_columns = [
    "original_cost_cr",
    "revised_cost_cr",
    "expenditure_cr",
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# Clean dates
# -----------------------------
date_columns = [
    "original_end_date",
    "revised_end_date",
]

for col in date_columns:
    df[col] = pd.to_datetime(
        df[col],
        format="%d/%m/%Y",
        errors="coerce"
    )

# -----------------------------
# Remove duplicate project codes
# -----------------------------
before = len(df)

df = df.drop_duplicates(
    subset=["project_code"],
    keep="first"
)

after = len(df)

print("Duplicate projects removed:", before - after)

# -----------------------------
# Basic missing-value handling
# -----------------------------
for col in ["sector", "ministry", "project_name"]:
    df[col] = df[col].fillna("Unknown")

# Numeric missing values
for col in numeric_columns:
    df[col] = df[col].fillna(0)

# -----------------------------
# Save cleaned dataset
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
# Summary
# -----------------------------
print("\nCleaning completed!")
print("Final shape:", df.shape)
print("Saved to:", OUTPUT_FILE)

print("\nMissing values:")
print(df.isnull().sum())