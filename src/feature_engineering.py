"""
Feature Engineering Pipeline for StockSense
=============================================
StockSense Round 2 - Step 1

This script loads data/processed/master_dataset.csv, constructs leak-free
time-series features (Lags, Rolling Statistics, Inventory Ratios, Price/Promo, Time),
computes the 7-day future demand target, and exports:
1. data/processed/features_dataset.csv
2. reports/feature_dictionary.md
"""

from pathlib import Path
import pandas as pd
import numpy as np


def get_project_root() -> Path:
    """Return the root path of the StockSense project."""
    return Path(__file__).resolve().parent.parent


def load_master_dataset(data_dir: Path) -> pd.DataFrame:
    """Load the processed master dataset created by Member 1."""
    master_path = data_dir / "master_dataset.csv"
    if not master_path.exists():
        raise FileNotFoundError(f"Master dataset not found at: {master_path}")
    df = pd.read_csv(master_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)
    return df


def compute_future_7day_demand(series: pd.Series) -> pd.Series:
    """
    Calculate the sum of daily_demand for the NEXT 7 days (t+1 to t+7)
    for a single store-product group ordered by date ascending.
    Ensures min_periods=7 so incomplete future windows result in NaN and are dropped.
    """
    rev = series.iloc[::-1]
    future_7day_sum = rev.shift(1).rolling(7, min_periods=7).sum().iloc[::-1]
    return future_7day_sum


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build time, lag, rolling, inventory, price, and target features cleanly without data leakage.
    """
    feat_df = df.copy()

    # -------------------------------------------------------------
    # 1. TIME FEATURES
    # -------------------------------------------------------------
    feat_df["day_of_week"] = feat_df["date"].dt.dayofweek
    feat_df["weekend_flag"] = (feat_df["day_of_week"] >= 5).astype(int)
    feat_df["month"] = feat_df["date"].dt.month
    feat_df["week_no"] = feat_df["date"].dt.isocalendar().week.astype(int)
    feat_df["festival_flag"] = feat_df["festival"].astype(int)

    # Ensure dataset is sorted by store_id, product_id, date before group operations
    feat_df = feat_df.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)
    group = feat_df.groupby(["store_id", "product_id"])

    # -------------------------------------------------------------
    # 2. LAG FEATURES (Strictly shift past values)
    # -------------------------------------------------------------
    feat_df["lag_1"] = group["daily_demand"].shift(1)
    feat_df["lag_7"] = group["daily_demand"].shift(7)
    feat_df["lag_14"] = group["daily_demand"].shift(14)

    # -------------------------------------------------------------
    # 3. ROLLING FEATURES (Shifted by 1 to exclude current day)
    # -------------------------------------------------------------
    feat_df["rolling_mean_7"] = group["daily_demand"].transform(
        lambda x: x.shift(1).rolling(7, min_periods=1).mean()
    )
    feat_df["rolling_mean_14"] = group["daily_demand"].transform(
        lambda x: x.shift(1).rolling(14, min_periods=1).mean()
    )
    feat_df["rolling_std_7"] = group["daily_demand"].transform(
        lambda x: x.shift(1).rolling(7, min_periods=1).std()
    ).fillna(0.0)

    # -------------------------------------------------------------
    # 4. INVENTORY & OPERATIONAL FEATURES
    # -------------------------------------------------------------
    # Days of inventory based on historical rolling 7-day mean demand
    feat_df["days_of_inventory"] = (
        feat_df["closing"] / (feat_df["rolling_mean_7"] + 1e-5)
    ).round(2)

    # Inventory to demand ratio (using lag_1 demand to prevent target leakage)
    feat_df["inventory_to_demand_ratio"] = (
        feat_df["closing"] / (feat_df["lag_1"] + 1.0)
    ).round(2)

    # Reorder gap (positive means below reorder level)
    feat_df["reorder_gap"] = feat_df["reorder_lvl"] - feat_df["closing"]

    # Alias shelf_life and lead_time for explicit naming consistency
    feat_df["shelf_life"] = feat_df["shelf_life_days"]
    feat_df["lead_time"] = feat_df["lead_days"]

    # -------------------------------------------------------------
    # 5. PRICE & PROMOTION FEATURES
    # -------------------------------------------------------------
    feat_df["discount_pct"] = feat_df["tx_avg_discount_pct"]
    feat_df["price_change"] = feat_df["mrp"] - feat_df["tx_effective_price"]
    feat_df["promotion_flag"] = feat_df["tx_promo_flag"]

    # -------------------------------------------------------------
    # 6. TARGET FEATURE: 7-DAY FUTURE DEMAND
    # -------------------------------------------------------------
    feat_df["next_7_day_demand"] = group["daily_demand"].transform(compute_future_7day_demand)

    # Drop rows where lag_14 is NaN or next_7_day_demand is NaN due to target window boundary
    # This ensures a fully populated, leak-free training dataset
    clean_feat_df = feat_df.dropna(subset=["lag_14", "next_7_day_demand"]).reset_index(drop=True)

    return clean_feat_df


def generate_feature_dictionary(output_path: Path):
    """Save feature_dictionary.md explaining every feature and leakage prevention."""
    doc_content = """# StockSense Feature Dictionary

This document describes all engineered features derived from `data/processed/master_dataset.csv` and details the strict anti-leakage safeguards applied.

---

## 1. Feature Specifications

| Feature Name | Category | Description | Anti-Leakage Safeguard |
| :--- | :--- | :--- | :--- |
| `day_of_week` | Time | Day of week index (0 = Mon, 6 = Sun) | Exact date calendar lookup |
| `weekend_flag` | Time | Binary indicator (1 if Sat/Sun, else 0) | Exact date calendar lookup |
| `month` | Time | Month index (1 to 12) | Exact date calendar lookup |
| `week_no` | Time | ISO week number | Exact date calendar lookup |
| `festival_flag` | Time | Binary flag for cultural/regional festival | Historical calendar event lookup |
| `lag_1` | Lag | `daily_demand` 1 day prior ($t-1$) | Shifted by +1 day |
| `lag_7` | Lag | `daily_demand` 7 days prior ($t-7$) | Shifted by +7 days |
| `lag_14` | Lag | `daily_demand` 14 days prior ($t-14$) | Shifted by +14 days |
| `rolling_mean_7` | Rolling | 7-day historical moving average demand | Computed on `shift(1)`, excluding day $t$ |
| `rolling_mean_14` | Rolling | 14-day historical moving average demand | Computed on `shift(1)`, excluding day $t$ |
| `rolling_std_7` | Rolling | 7-day historical demand standard deviation | Computed on `shift(1)`, excluding day $t$ |
| `days_of_inventory` | Inventory | $Closing / (RollingMean7 + 1e-5)$ | Uses historical rolling average demand |
| `inventory_to_demand_ratio` | Inventory | $Closing / (Lag1 + 1)$ | Uses lag_1 demand, excluding current/future demand |
| `reorder_gap` | Inventory | $ReorderLvl - Closing$ | Uses end-of-day closing stock |
| `discount_pct` | Price/Promo | Average transaction discount percentage | Recorded POS transaction attribute for day $t$ |
| `price_change` | Price/Promo | Difference between MRP and effective price | Recorded POS pricing metric |
| `promotion_flag` | Price/Promo | Binary indicator if promotion was active | Recorded POS promotion flag |
| `store_type` | Categorical | Format of store (Supermarket, Hypermarket, Express) | Static store master attribute |
| `category` | Categorical | Unified product category | Static product master attribute |
| `brand` | Categorical | Product brand name | Static product master attribute |
| `shelf_life` | Operational | Product shelf life in days | Static product master attribute |
| `lead_time` | Operational | Supplier lead time in days | Static product master attribute |
| **`next_7_day_demand`** | **Target** | Sum of `daily_demand` from $t+1$ to $t+7$ | Calculated strictly forward in time |

---

## 2. Anti-Leakage Protocol

1. **Grouped Time-Series Ordering**: All lag and rolling transformations are calculated per `(store_id, product_id)` group sorted chronologically by `date`.
2. **Prior Window Exclusion (`shift(1)`)**: Rolling statistics (`rolling_mean_7`, `rolling_mean_14`, `rolling_std_7`) are explicitly calculated over `.shift(1)` to ensure demand on day $t$ or future days is never included in input features.
3. **Boundary Truncation**: Rows with missing historical lags (first 14 days of history) or missing future target windows (last 7 days of dataset) are cleanly pruned.
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(doc_content)
    print(f"Feature dictionary successfully saved to: {output_path}")


def main():
    root = get_project_root()
    data_dir = root / "data" / "processed"
    reports_dir = root / "reports"

    # Step 1: Load master dataset
    raw_df = load_master_dataset(data_dir)
    print(f"Loaded master dataset: {raw_df.shape[0]} rows x {raw_df.shape[1]} columns")

    # Step 2: Build features
    features_df = build_features(raw_df)

    # Step 3: Export features_dataset.csv
    features_csv_path = data_dir / "features_dataset.csv"
    features_df.to_csv(features_csv_path, index=False)
    print(f"Features dataset successfully exported to: {features_csv_path} ({features_df.shape[0]} rows x {features_df.shape[1]} columns)")

    # Step 4: Export feature_dictionary.md
    generate_feature_dictionary(reports_dir / "feature_dictionary.md")


if __name__ == "__main__":
    main()
