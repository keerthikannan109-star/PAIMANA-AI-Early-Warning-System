import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

from pathlib import Path

# ---------------------------------------
# Paths
# ---------------------------------------
MODEL_FILE = Path("models/cost_overrun_xgboost.pkl")
DATA_FILE = Path("data/processed/paimana_cleaned.csv")
OUTPUT_DIR = Path("outputs")

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------
# Load model and data
# ---------------------------------------
model = joblib.load(MODEL_FILE)
df = pd.read_csv(DATA_FILE)

# ---------------------------------------
# Prepare data
# ---------------------------------------
X = df[
    [
        "original_cost_cr",
        "sector",
        "ministry"
    ]
].copy()

# ---------------------------------------
# Transform data using pipeline
# ---------------------------------------
preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]

X_transformed = preprocessor.transform(X)

# Get feature names
feature_names = preprocessor.get_feature_names_out()

# Convert sparse matrix if required
if hasattr(X_transformed, "toarray"):
    X_transformed = X_transformed.toarray()

X_transformed = pd.DataFrame(
    X_transformed,
    columns=feature_names
)

# ---------------------------------------
# SHAP Explainer
# ---------------------------------------
explainer = shap.TreeExplainer(classifier)

shap_values = explainer.shap_values(
    X_transformed
)

# ---------------------------------------
# SHAP Summary Plot
# ---------------------------------------
plt.figure()

shap.summary_plot(
    shap_values,
    X_transformed,
    show=False
)

plt.tight_layout()

output_file = OUTPUT_DIR / "shap_cost_overrun_summary.png"

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\n================================")
print("SHAP ANALYSIS COMPLETED")
print("================================")

print("SHAP plot saved to:")
print(output_file)