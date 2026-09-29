# StockSense Feature Dictionary

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
