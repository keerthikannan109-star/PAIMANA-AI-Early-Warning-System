from flask import Flask, render_template
from pathlib import Path
import pandas as pd

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "project_risk_predictions.csv"
)


@app.route("/")
def dashboard():

    if not DATA_FILE.exists():
        return f"Data file not found: {DATA_FILE}"

    df = pd.read_csv(DATA_FILE)

    # =========================================
    # BASIC DATA CLEANING
    # =========================================

    df["risk_score"] = pd.to_numeric(
        df["risk_score"],
        errors="coerce"
    ).fillna(0)

    df["cost_risk_probability"] = pd.to_numeric(
        df["cost_risk_probability"],
        errors="coerce"
    ).fillna(0)

    df["time_risk_probability"] = pd.to_numeric(
        df["time_risk_probability"],
        errors="coerce"
    ).fillna(0)

    # =========================================
    # KPI CALCULATIONS
    # =========================================

    total_projects = len(df)

    critical_projects = int(
        (df["risk_level"] == "Critical").sum()
    )

    high_projects = int(
        (df["risk_level"] == "High").sum()
    )

    medium_projects = int(
        (df["risk_level"] == "Medium").sum()
    )

    low_projects = int(
        (df["risk_level"] == "Low").sum()
    )

    average_risk = round(
        df["risk_score"].mean(),
        2
    )

    # =========================================
    # RISK PERCENTAGES
    # =========================================

    if total_projects > 0:

        critical_percent = (
            critical_projects / total_projects
        ) * 100

        high_percent = (
            high_projects / total_projects
        ) * 100

        medium_percent = (
            medium_projects / total_projects
        ) * 100

        low_percent = (
            low_projects / total_projects
        ) * 100

    else:

        critical_percent = 0
        high_percent = 0
        medium_percent = 0
        low_percent = 0

    # =========================================
    # AI ANALYTICS
    # =========================================

    # Average predicted cost risk
    average_cost_risk = round(
        df["cost_risk_probability"].mean() * 100,
        1
    )

    # Average predicted time risk
    average_time_risk = round(
        df["time_risk_probability"].mean() * 100,
        1
    )

    # Number of projects with cost warning
    cost_warning_projects = int(
        (
            df["cost_risk_probability"] >= 0.60
        ).sum()
    )

    # Number of projects with time warning
    time_warning_projects = int(
        (
            df["time_risk_probability"] >= 0.60
        ).sum()
    )

    # Number of projects requiring both warnings
    combined_warning_projects = int(
        (
            (df["cost_risk_probability"] >= 0.60)
            &
            (df["time_risk_probability"] >= 0.60)
        ).sum()
    )

    # =========================================
    # SECTOR ANALYTICS
    # =========================================

    sector_summary = (
        df.groupby("sector")
        .agg(
            project_count=("project_code", "count"),
            average_risk=("risk_score", "mean"),
            average_cost_risk=(
                "cost_risk_probability",
                "mean"
            ),
            average_time_risk=(
                "time_risk_probability",
                "mean"
            )
        )
        .reset_index()
    )

    sector_summary["average_risk"] = (
        sector_summary["average_risk"]
        .round(2)
    )

    sector_summary["average_cost_risk"] = (
        sector_summary["average_cost_risk"] * 100
    ).round(1)

    sector_summary["average_time_risk"] = (
        sector_summary["average_time_risk"] * 100
    ).round(1)

    # Sort highest-risk sectors first
    sector_summary = sector_summary.sort_values(
        by="average_risk",
        ascending=False
    )

    # =========================================
    # TOP HIGH-RISK PROJECTS
    # =========================================

    top_risk_df = (
        df.sort_values(
            by="risk_score",
            ascending=False
        )
        .head(10)
    )

    top_risk_projects = top_risk_df[
        [
            "project_code",
            "project_name",
            "sector",
            "risk_score",
            "risk_level",
            "cost_risk_probability",
            "time_risk_probability"
        ]
    ].copy()

    top_risk_projects["risk_score"] = (
        top_risk_projects["risk_score"]
        .round(2)
    )

    top_risk_projects["cost_risk_probability"] = (
        top_risk_projects["cost_risk_probability"] * 100
    ).round(1)

    top_risk_projects["time_risk_probability"] = (
        top_risk_projects["time_risk_probability"] * 100
    ).round(1)

    top_risk_projects = top_risk_projects.to_dict(
        orient="records"
    )

    # =========================================
    # PROJECT DATA
    # =========================================

    project_columns = [
        "project_code",
        "project_name",
        "sector",
        "ministry",
        "original_cost_cr",
        "revised_cost_cr",
        "expenditure_cr",
        "original_end_date",
        "revised_end_date",
        "risk_score",
        "cost_risk_probability",
        "time_risk_probability",
        "risk_level",
        "early_warning"
    ]

    projects_df = df[project_columns].copy()

    # =========================================
    # DISPLAY FORMATTING
    # =========================================

    projects_df["risk_score"] = (
        projects_df["risk_score"].round(2)
    )

    projects_df["cost_risk_probability"] = (
        projects_df["cost_risk_probability"] * 100
    ).round(1)

    projects_df["time_risk_probability"] = (
        projects_df["time_risk_probability"] * 100
    ).round(1)

    # =========================================
    # PROJECT DICTIONARY
    # =========================================

    projects = projects_df.to_dict(
        orient="records"
    )

    # =========================================
    # SECTOR DICTIONARY
    # =========================================

    sector_analytics = sector_summary.to_dict(
        orient="records"
    )

    # =========================================
    # SEND DATA TO HTML
    # =========================================

    return render_template(
        "index.html",

        # KPI
        total_projects=total_projects,

        critical_projects=critical_projects,

        high_projects=high_projects,

        medium_projects=medium_projects,

        low_projects=low_projects,

        average_risk=average_risk,

        # Risk percentages
        critical_percent=round(
            critical_percent,
            2
        ),

        high_percent=round(
            high_percent,
            2
        ),

        medium_percent=round(
            medium_percent,
            2
        ),

        low_percent=round(
            low_percent,
            2
        ),

        # AI analytics
        average_cost_risk=average_cost_risk,

        average_time_risk=average_time_risk,

        cost_warning_projects=cost_warning_projects,

        time_warning_projects=time_warning_projects,

        combined_warning_projects=combined_warning_projects,

        # Sector analytics
        sector_analytics=sector_analytics,

        # Top risk projects
        top_risk_projects=top_risk_projects,

        # Project table
        projects=projects
    )


# =========================================
# RUN FLASK APPLICATION
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )