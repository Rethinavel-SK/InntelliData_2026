"""
Recommendation Engine & Decision Output Generator for StockSense
================================================================
StockSense Round 2 - Step 5

Combines 7-day demand forecasts, stock-out probability models, and safety stock economics
to compute optimal inventory reorder quantities and actionable manager recommendations.

Business Formulas:
- Safety Stock = ceil(Z * std_demand * sqrt(lead_days)) where Z = 1.65 (95% service level)
- Recommended Stock = Forecast 7-Day Demand + Safety Stock
- Recommended Order Quantity = max(0, Recommended Stock - Current Stock - Incoming Stock)

Exports:
- data/processed/recommendations.csv
- data/processed/stocksense_decision_output.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np
import joblib


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def generate_manager_action(risk_level: str, reorder_qty: int) -> str:
    """Generate prescriptive actions for store managers based on risk and reorder quantities."""
    if risk_level == "HIGH" or reorder_qty > 0:
        if reorder_qty > 100:
            return "CRITICAL: Issue emergency purchase order immediately to prevent stockout"
        return "URGENT: Place purchase order within 24 hours to replenish stock"
    elif risk_level == "MEDIUM":
        return "MONITOR: Schedule stock replenishment order in next ordering cycle"
    else:
        return "NORMAL: Stock levels optimal; maintain regular replenishment schedule"


def main():
    root = get_project_root()
    data_dir = root / "data" / "processed"
    models_dir = root / "models"
    reports_dir = root / "reports"

    # Step 1: Load features dataset
    features_df = pd.read_csv(data_dir / "features_dataset.csv")
    features_df["date"] = pd.to_datetime(features_df["date"])

    # Step 2: Load trained Demand Forecasting model
    forecast_model_path = models_dir / "demand_forecast_model.joblib"
    if not forecast_model_path.exists():
        raise FileNotFoundError(f"Forecast model not found at: {forecast_model_path}")
    
    forecast_payload = joblib.load(forecast_model_path)
    reg_model = forecast_payload["model"]
    reg_scaler = forecast_payload.get("scaler", None)
    reg_feature_names = forecast_payload["feature_names"]

    # Step 3: Load trained Stockout Classification model
    stockout_model_path = models_dir / "stockout_prediction_model.joblib"
    if not stockout_model_path.exists():
        raise FileNotFoundError(f"Stockout model not found at: {stockout_model_path}")

    stockout_payload = joblib.load(stockout_model_path)
    clf_model = stockout_payload["model"]
    clf_scaler = stockout_payload.get("scaler", None)
    clf_feature_names = stockout_payload["feature_names"]

    # Step 4: Generate Demand Forecast (7-day ahead)
    # Prepare feature encoded matrices for prediction
    cat_cols = ["store_id", "product_id", "store_type", "category", "brand"]
    encoded_reg = pd.get_dummies(features_df, columns=cat_cols, drop_first=True)
    
    # Align columns with model feature_names
    for col in reg_feature_names:
        if col not in encoded_reg.columns:
            encoded_reg[col] = 0.0
    X_reg = encoded_reg[reg_feature_names].astype(float)

    if reg_scaler is not None and hasattr(reg_model, "coef_"):
        X_reg_scaled = reg_scaler.transform(X_reg)
        pred_demand = reg_model.predict(X_reg_scaled)
    else:
        pred_demand = reg_model.predict(X_reg)

    features_df["forecasted_7day_demand"] = np.maximum(0, np.round(pred_demand)).astype(int)

    # Step 5: Generate Stock-out Risk Probability
    encoded_clf = pd.get_dummies(features_df, columns=cat_cols, drop_first=True)
    for col in clf_feature_names:
        if col not in encoded_clf.columns:
            encoded_clf[col] = 0.0
    X_clf = encoded_clf[clf_feature_names].astype(float)

    if clf_scaler is not None and not hasattr(clf_model, "feature_importances_"):
        X_clf_scaled = clf_scaler.transform(X_clf)
        prob_stockout = clf_model.predict_proba(X_clf_scaled)[:, 1]
    else:
        prob_stockout = clf_model.predict_proba(X_clf)[:, 1]

    features_df["stockout_probability"] = np.round(prob_stockout, 4)

    # Step 6: Assign Risk Levels
    def assign_risk_level(prob: float) -> str:
        if prob >= 0.70:
            return "HIGH"
        elif prob >= 0.40:
            return "MEDIUM"
        else:
            return "LOW"

    features_df["risk_level"] = features_df["stockout_probability"].apply(assign_risk_level)

    # Step 7: Inventory Economics & Safety Stock Calculation
    # Formula: Safety Stock = ceil(Z * std_demand * sqrt(lead_days)) (Z = 1.65 for 95% service level)
    Z_score = 1.65
    std_demand = features_df["rolling_std_7"].replace(0, 5.0)
    lead_days = features_df["lead_time"]

    features_df["safety_stock"] = np.ceil(Z_score * std_demand * np.sqrt(lead_days)).astype(int)
    features_df["recommended_stock"] = features_df["forecasted_7day_demand"] + features_df["safety_stock"]

    # Current Stock = closing, Incoming Stock = received
    current_stock = features_df["closing"]
    incoming_stock = features_df["received"]

    # Recommended Order Quantity = max(0, Recommended Stock - Current Stock - Incoming Stock)
    features_df["recommended_order_qty"] = np.maximum(
        0, features_df["recommended_stock"] - current_stock - incoming_stock
    ).astype(int)

    # Load explanation reasons
    explain_csv = reports_dir / "explainability_summary.csv"
    if explain_csv.exists():
        exp_df = pd.read_csv(explain_csv)
        features_df["key_reasons"] = exp_df["explanation_reasons"]
    else:
        features_df["key_reasons"] = "Stock level evaluated against forecasted demand and lead time"

    # Manager Actions
    features_df["manager_action"] = features_df.apply(
        lambda r: generate_manager_action(r["risk_level"], r["recommended_order_qty"]), axis=1
    )

    # Step 8: Build Final Recommendations Table
    rec_cols = [
        "date", "store_id", "product_id", "category", "brand",
        "closing", "received", "forecasted_7day_demand", "safety_stock",
        "stockout_probability", "risk_level", "recommended_order_qty",
        "key_reasons", "manager_action"
    ]

    rec_df = features_df[rec_cols].copy().rename(columns={
        "store_id": "Store",
        "product_id": "Product",
        "category": "Category",
        "brand": "Brand",
        "closing": "Current_Stock",
        "received": "Incoming_Stock",
        "forecasted_7day_demand": "7_Day_Forecast",
        "safety_stock": "Safety_Stock",
        "stockout_probability": "Stockout_Probability",
        "risk_level": "Risk_Level",
        "recommended_order_qty": "Recommended_Order_Qty",
        "key_reasons": "Key_Reasons",
        "manager_action": "Manager_Action"
    })

    rec_df = rec_df.sort_values(["date", "Risk_Level", "Recommended_Order_Qty"], ascending=[True, True, False]).reset_index(drop=True)

    # Export recommendations.csv
    rec_csv_path = data_dir / "recommendations.csv"
    rec_df.to_csv(rec_csv_path, index=False)
    print(f"Recommendations exported to: {rec_csv_path} ({len(rec_df)} rows)")

    # Export full decision dataset
    decision_path = data_dir / "stocksense_decision_output.csv"
    features_df.to_csv(decision_path, index=False)
    print(f"Full decision output dataset exported to: {decision_path} ({len(features_df)} rows x {len(features_df.columns)} cols)")

    # Print top recommendation sample
    print("\n--- Top Sample Recommendations (Latest Date) ---")
    latest_date = rec_df["date"].max()
    sample = rec_df[rec_df["date"] == latest_date].head(8)
    print(sample[["Store", "Product", "Category", "Current_Stock", "7_Day_Forecast", "Risk_Level", "Recommended_Order_Qty", "Manager_Action"]].to_string(index=False))


if __name__ == "__main__":
    main()
