"""
Demand Forecasting Module for StockSense
========================================
StockSense Round 2 - Step 2

Trains and compares 7 regression models on 7-day future demand:
1. Baseline (7-Day Rolling Historical Demand Sum)
2. Linear Regression
3. Decision Tree Regressor
4. Random Forest Regressor
5. XGBoost Regressor
6. K-Nearest Neighbors (KNN) Regressor
7. Support Vector Regressor (SVR)

Strictly uses time-aware train/test splitting (first 80% dates for training, last 20% for testing).
Evaluates models using MAE, RMSE, MAPE, and R².
Saves:
- reports/demand_model_comparison.csv
- models/demand_forecast_model.joblib
- reports/demand_feature_importance.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def compute_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute Mean Absolute Percentage Error (%) ignoring zero denominators."""
    mask = y_true != 0
    if not np.any(mask):
        return 0.0
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100.0)


def prepare_data(df: pd.DataFrame):
    """
    Prepare feature matrix X and target y with time-based train/test split.
    """
    df = df.sort_values("date").reset_index(drop=True)

    target_col = "next_7_day_demand"
    ignore_cols = ["date", "daily_demand", target_col]

    # Selected predictor columns
    numeric_cols = [
        "day_of_week", "weekend_flag", "month", "week_no", "festival_flag",
        "lag_1", "lag_7", "lag_14", "rolling_mean_7", "rolling_mean_14", "rolling_std_7",
        "days_of_inventory", "inventory_to_demand_ratio", "reorder_gap",
        "discount_pct", "price_change", "promotion_flag", "shelf_life", "lead_time",
        "opening", "closing", "received", "reorder_lvl"
    ]

    categorical_cols = ["store_id", "product_id", "store_type", "category", "brand"]

    # Filter available columns
    num_cols = [c for c in numeric_cols if c in df.columns]
    cat_cols = [c for c in categorical_cols if c in df.columns]

    # One-hot encode categorical features
    df_encoded = pd.get_dummies(df[num_cols + cat_cols], columns=cat_cols, drop_first=True)
    feature_names = list(df_encoded.columns)

    X = df_encoded.astype(float)
    y = df[target_col].values

    # Time-based split: train on early 80% dates, test on last 20% dates
    unique_dates = sorted(df["date"].unique())
    split_idx = int(len(unique_dates) * 0.8)
    cutoff_date = unique_dates[split_idx]

    train_mask = df["date"] < cutoff_date
    test_mask = df["date"] >= cutoff_date

    X_train, y_train = X[train_mask], y[train_mask]
    X_test, y_test = X[test_mask], y[test_mask]

    print(f"Data Split Summary:")
    print(f"  Train set: {len(X_train)} samples (Dates: {df['date'].min().strftime('%Y-%m-%d')} to {df[train_mask]['date'].max().strftime('%Y-%m-%d')})")
    print(f"  Test set : {len(X_test)} samples (Dates: {cutoff_date.strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')})")

    return X_train, y_train, X_test, y_test, feature_names, df[test_mask].reset_index(drop=True)


def train_and_evaluate_models(X_train, y_train, X_test, y_test, feature_names, test_df):
    """
    Train 7 regression models and evaluate metrics.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 1. Baseline: Previous 7-day rolling sum (rolling_mean_7 * 7)
    baseline_pred = np.maximum(0, test_df["rolling_mean_7"].values * 7.0)
    
    models = {
        "Baseline (7-Day Rolling Sum)": None,
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(max_depth=6, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42),
        "XGBoost": XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.05, random_state=42),
        "KNN Regressor": KNeighborsRegressor(n_neighbors=5),
        "Support Vector Regressor (SVR)": SVR(C=10.0, epsilon=1.0)
    }

    results = []
    trained_models = {}

    for name, model in models.items():
        if name == "Baseline (7-Day Rolling Sum)":
            y_pred = baseline_pred
        else:
            if name in ["Linear Regression", "KNN Regressor", "Support Vector Regressor (SVR)"]:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
            
            y_pred = np.maximum(0, y_pred)  # Non-negative constraint
            trained_models[name] = model

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mape = compute_mape(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        results.append({
            "model": name,
            "mae": round(float(mae), 2),
            "rmse": round(float(rmse), 2),
            "mape_pct": round(float(mape), 2),
            "r2_score": round(float(r2), 4)
        })

    results_df = pd.DataFrame(results).sort_values("mae").reset_index(drop=True)

    # Select best model (excluding baseline)
    ml_results = results_df[results_df["model"] != "Baseline (7-Day Rolling Sum)"]
    best_model_name = ml_results.iloc[0]["model"]
    best_model = trained_models[best_model_name]

    print("\n--- Demand Forecasting Model Comparison ---")
    print(results_df.to_string(index=False))
    print(f"\nBest Selected Forecasting Model: {best_model_name}")

    # Extract feature importance if available
    feature_importance_df = pd.DataFrame()
    if hasattr(best_model, "feature_importances_"):
        importances = best_model.feature_importances_
        feature_importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance": importances
        }).sort_values("importance", ascending=False).reset_index(drop=True)
    elif hasattr(best_model, "coef_"):
        importances = np.abs(best_model.coef_)
        feature_importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance": importances
        }).sort_values("importance", ascending=False).reset_index(drop=True)

    return results_df, best_model_name, best_model, feature_importance_df, scaler


def main():
    root = get_project_root()
    data_dir = root / "data" / "processed"
    models_dir = root / "models"
    reports_dir = root / "reports"

    models_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Load features dataset
    features_df = pd.read_csv(data_dir / "features_dataset.csv")
    features_df["date"] = pd.to_datetime(features_df["date"])

    # Step 2: Prepare data & splits
    X_train, y_train, X_test, y_test, feature_names, test_df = prepare_data(features_df)

    # Step 3: Train and evaluate models
    results_df, best_model_name, best_model, feature_importance_df, scaler = train_and_evaluate_models(
        X_train, y_train, X_test, y_test, feature_names, test_df
    )

    # Step 4: Export comparison report
    results_df.to_csv(reports_dir / "demand_model_comparison.csv", index=False)
    print(f"Model comparison saved to: {reports_dir / 'demand_model_comparison.csv'}")

    # Step 5: Save best model & pipeline artifacts
    model_payload = {
        "model_name": best_model_name,
        "model": best_model,
        "scaler": scaler,
        "feature_names": feature_names
    }
    model_path = models_dir / "demand_forecast_model.joblib"
    joblib.dump(model_payload, model_path)
    print(f"Best model successfully saved to: {model_path}")

    # Step 6: Save feature importances
    if not feature_importance_df.empty:
        importance_path = reports_dir / "demand_feature_importance.csv"
        feature_importance_df.to_csv(importance_path, index=False)
        print(f"Feature importance saved to: {importance_path}")


if __name__ == "__main__":
    main()
