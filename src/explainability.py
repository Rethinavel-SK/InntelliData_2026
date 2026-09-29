"""
Explainability Engine for StockSense Stock-Out Prediction
==========================================================
StockSense Round 2 - Step 4

Extracts feature importances from the trained stock-out classification model,
evaluates key drivers for each Store x Product risk evaluation, and generates
human-readable explanation reasons.

Exports:
- reports/explainability_summary.csv
- reports/explainability_summary.md
"""

from pathlib import Path
import pandas as pd
import numpy as np
import joblib


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def generate_explanation_reason(row: pd.Series, top_features: list[str]) -> str:
    """
    Generate human-readable explanations based on feature values and top model drivers.
    """
    reasons = []

    closing = row.get("closing", 0)
    reorder_lvl = row.get("reorder_lvl", 0)
    forecast = row.get("next_7_day_demand", 0)
    days_inv = row.get("days_of_inventory", 0.0)
    lead_time = row.get("lead_time", row.get("lead_days", 0))

    if closing <= reorder_lvl:
        reasons.append(f"Current closing stock ({int(closing)} units) is at or below reorder threshold ({int(reorder_lvl)} units)")

    if days_inv < 3.0:
        reasons.append(f"Critically low days of inventory ({days_inv:.1f} days remaining based on 7-day trend)")

    if forecast > closing:
        reasons.append(f"7-day forecasted demand ({int(forecast)} units) exceeds available stock ({int(closing)} units)")

    if lead_time >= 3:
        reasons.append(f"Supplier replenishment lead time is relatively high ({int(lead_time)} days)")

    if not reasons:
        reasons.append("Inventory levels are sufficient to satisfy historical and forecasted customer demand")

    return " | ".join(reasons)


def main():
    root = get_project_root()
    data_dir = root / "data" / "processed"
    models_dir = root / "models"
    reports_dir = root / "reports"

    # Step 1: Load classification model payload
    model_path = models_dir / "stockout_prediction_model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(f"Stockout model not found at: {model_path}")

    payload = joblib.load(model_path)
    model = payload["model"]
    feature_names = payload["feature_names"]
    scaler = payload.get("scaler", None)

    # Step 2: Extract feature importances
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0])
    else:
        importances = np.ones(len(feature_names)) / len(feature_names)

    feature_imp_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    }).sort_values("importance", ascending=False).reset_index(drop=True)

    print("\n--- Stock-out Model Feature Importances ---")
    print(feature_imp_df.head(10).to_string(index=False))

    # Save feature importance csv
    feature_imp_df.to_csv(reports_dir / "stockout_feature_importance.csv", index=False)

    # Step 3: Load features dataset to generate row-level explanations
    features_df = pd.read_csv(data_dir / "features_dataset.csv")

    # Generate explanations
    top_driver_names = feature_imp_df["feature"].head(5).tolist()
    features_df["explanation_reasons"] = features_df.apply(
        lambda row: generate_explanation_reason(row, top_driver_names), axis=1
    )

    # Select columns for summary
    summary_cols = [
        "date", "store_id", "product_id", "category", "brand", "closing", "reorder_lvl",
        "lead_time", "days_of_inventory", "next_7_day_demand", "explanation_reasons"
    ]
    summary_cols = [c for c in summary_cols if c in features_df.columns]
    summary_df = features_df[summary_cols].copy()

    # Save CSV summary
    summary_csv_path = reports_dir / "explainability_summary.csv"
    summary_df.to_csv(summary_csv_path, index=False)
    print(f"Explainability summary CSV saved to: {summary_csv_path}")

    # Generate Markdown Summary
    md_content = f"""# StockSense Model Explainability Report

## 1. Top Global Feature Drivers (Stock-out Risk)

| Rank | Feature | Importance Score | Business Impact Description |
| :---: | :--- | :---: | :--- |
"""
    for idx, row in feature_imp_df.head(8).iterrows():
        md_content += f"| {idx+1} | `{row['feature']}` | {row['importance']:.4f} | Driver of stockout risk classification decision |\n"

    md_content += """
---

## 2. Sample Explanation Reasons (Store × Product Level)

"""
    sample_df = summary_df.tail(10)
    for _, row in sample_df.iterrows():
        md_content += f"- **Store `{row['store_id']}` | Product `{row['product_id']}` ({row.get('category', '')})** [{row['date']}]\n"
        md_content += f"  - Stock: `{int(row['closing'])}` units | Reorder Level: `{int(row['reorder_lvl'])}` units | 7-Day Forecast: `{int(row['next_7_day_demand'])}` units\n"
        md_content += f"  - **Key Reasons**: {row['explanation_reasons']}\n\n"

    md_path = reports_dir / "explainability_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Explainability summary MD saved to: {md_path}")


if __name__ == "__main__":
    main()
