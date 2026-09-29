# STOCKSENSE (IntelliData 2026) - Member 2 Executive Summary & Validation Report

## 1. Overview of Deliverables Created

| Category | File Path | Description |
| :--- | :--- | :--- |
| **Pipeline Scripts** | [`src/feature_engineering.py`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/src/feature_engineering.py) | Leak-free time-series & inventory feature creation pipeline |
| | [`src/demand_forecasting.py`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/src/demand_forecasting.py) | 7-day future demand regression modeling and comparison engine |
| | [`src/stockout_prediction.py`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/src/stockout_prediction.py) | Stock-out risk classification engine and probability estimator |
| | [`src/explainability.py`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/src/explainability.py) | Model interpretability & store-level explanation reason generator |
| | [`src/recommendation_engine.py`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/src/recommendation_engine.py) | Safety stock economics & optimal order recommendation engine |
| **Processed Datasets** | [`data/processed/features_dataset.csv`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/data/processed/features_dataset.csv) | Full dataset with engineered features (400 rows × 60 columns) |
| | [`data/processed/recommendations.csv`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/data/processed/recommendations.csv) | Business decision table with reorder quantities and manager actions |
| | [`data/processed/stocksense_decision_output.csv`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/data/processed/stocksense_decision_output.csv) | Unified decision dataset for UI/Dashboard consumption |
| **Trained Models** | [`models/demand_forecast_model.joblib`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/models/demand_forecast_model.joblib) | Serialized Random Forest Regressor & scaling pipeline |
| | [`models/stockout_prediction_model.joblib`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/models/stockout_prediction_model.joblib) | Serialized Decision Tree Classifier & scaling pipeline |
| **Reports & Figures** | [`reports/feature_dictionary.md`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/reports/feature_dictionary.md) | Feature catalog and data leakage prevention documentation |
| | [`reports/demand_model_comparison.csv`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/reports/demand_model_comparison.csv) | Performance benchmark of 7 demand forecasting models |
| | [`reports/demand_feature_importance.csv`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/reports/demand_feature_importance.csv) | Feature importances for demand forecasting |
| | [`reports/stockout_model_comparison.csv`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/reports/stockout_model_comparison.csv) | Performance benchmark of 7 stock-out classification models |
| | [`reports/stockout_feature_importance.csv`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/reports/stockout_feature_importance.csv) | Feature importances for stock-out classification |
| | [`reports/figures/stockout_confusion_matrix.png`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/reports/figures/stockout_confusion_matrix.png) | High-resolution confusion matrix heatmap for classification |
| | [`reports/explainability_summary.csv`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/reports/explainability_summary.csv) | Store × Product level key explanation reasons |
| | [`reports/explainability_summary.md`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/reports/explainability_summary.md) | Human-readable markdown report for model explainability |

---

## 2. Engineered Features Summary

- **Time Features**: `day_of_week`, `weekend_flag`, `month`, `week_no`, `festival_flag`
- **Lag Features**: `lag_1`, `lag_7`, `lag_14` (shifted per store-product group)
- **Rolling Features**: `rolling_mean_7`, `rolling_mean_14`, `rolling_std_7` (calculated over `.shift(1)` to eliminate leakage)
- **Inventory Metrics**: `days_of_inventory` ($Closing / RollingMean7$), `inventory_to_demand_ratio` ($Closing / (Lag1 + 1)$), `reorder_gap` ($ReorderLvl - Closing$)
- **Price & Promo**: `discount_pct`, `price_change` ($MRP - EffectivePrice$), `promotion_flag`
- **Store & Product**: `store_type`, `category`, `brand`, `shelf_life`, `lead_time`, `opening`, `closing`
- **Target**: `next_7_day_demand` (Sum of `daily_demand` over days $t+1$ to $t+7$)

---

## 3. Demand Forecasting Model Comparison (Real Computed Values)

| Model Name | MAE (units) | RMSE (units) | MAPE (%) | $R^2$ Score |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest Regressor (SELECTED)** | **17.36** | **23.09** | **3.08%** | **0.9947** |
| Decision Tree Regressor | 19.64 | 28.88 | 3.39% | 0.9918 |
| K-Nearest Neighbors (KNN) | 25.79 | 36.17 | 4.99% | 0.9871 |
| Linear Regression | 25.99 | 31.82 | 7.58% | 0.9900 |
| Baseline (7-Day Rolling Sum) | 27.36 | 35.39 | 5.25% | 0.9876 |
| XGBoost Regressor | 28.92 | 51.76 | 5.08% | 0.9735 |
| Support Vector Regressor (SVR) | 127.84 | 175.19 | 44.25% | 0.6969 |

**Selected Forecast Model**: **Random Forest Regressor** (`MAE = 17.36 units`, `R² = 0.9947`).

---

## 4. Stock-out Risk Classification Model Comparison (Real Computed Values)

| Model Name | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Decision Tree Classifier (SELECTED)** | **96.25%** | **95.52%** | **100.00%** | **0.9771** | **0.9062** |
| Random Forest Classifier | 96.25% | 96.92% | 98.44% | 0.9767 | 0.9863 |
| XGBoost Classifier | 95.00% | 95.45% | 98.44% | 0.9692 | 0.9893 |
| Logistic Regression | 95.00% | 96.88% | 96.88% | 0.9688 | 0.9912 |
| Support Vector Machine (SVC) | 91.25% | 93.85% | 95.31% | 0.9457 | 0.9658 |
| Naive Bayes Classifier | 90.00% | 92.42% | 95.31% | 0.9385 | 0.8721 |
| KNN Classifier | 88.75% | 87.67% | 100.00% | 0.9343 | 0.9067 |

**Selected Stock-out Model**: **Decision Tree Classifier** (`Accuracy = 96.25%`, `Recall = 100%`, `F1 = 0.9771`).

---

## 5. Top Feature Drivers (Global Importance)

1. `inventory_to_demand_ratio` (Importance: **0.8172**): Primary driver of stock-out probability.
2. `days_of_inventory` (Importance: **0.0683**): Forward coverage indicator.
3. `opening` (Importance: **0.0467**): Day start stock availability.
4. `reorder_lvl` (Importance: **0.0305**): Baseline replenishment threshold.
5. `rolling_std_7` (Importance: **0.0253**): Volatility in 7-day customer demand.

---

## 6. Sample Recommendation Outputs

| Store | Product | Category | Current Stock | 7-Day Forecast | Safety Stock | Risk Level | Reorder Qty | Prescriptive Manager Action |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **S01** | **P330** | Beverages | 136 | 921 | 38 | **HIGH** | **823** | CRITICAL: Issue emergency purchase order immediately to prevent stockout |
| **S04** | **P330** | Beverages | 59 | 835 | 34 | **HIGH** | **810** | CRITICAL: Issue emergency purchase order immediately to prevent stockout |
| **S01** | **P101** | Dairy | 66 | 731 | 26 | **HIGH** | **691** | CRITICAL: Issue emergency purchase order immediately to prevent stockout |
| **S04** | **P101** | Dairy | 60 | 679 | 47 | **HIGH** | **666** | CRITICAL: Issue emergency purchase order immediately to prevent stockout |
| **S02** | **P442** | Snacks | 165 | 826 | 40 | **HIGH** | **601** | CRITICAL: Issue emergency purchase order immediately to prevent stockout |

---

## 7. Validation Checklist

- [x] **No Data Leakage**: All rolling features computed on `.shift(1)`; target calculated purely forward ($t+1$ to $t+7$).
- [x] **Time-Aware Split**: Chronological split (first 80% dates for training, last 20% for testing).
- [x] **No Negative Quantities**: All demand forecasts and reorder quantities strictly clamped at $\ge 0$.
- [x] **Model Loadability**: Verified `joblib.load()` succeeds for both regression and classification payloads.
- [x] **No Deep Learning**: Adhered strictly to permitted ML algorithms (Random Forest, Decision Tree, Linear Regression, XGBoost, KNN, Naive Bayes, SVM).
- [x] **Additive Repo Work**: Member 1 files untouched; all new modules cleanly integrated into `src/`, `models/`, `reports/`, and `data/processed/`.

---

## 8. Handoff Notes for Member 1 & Member 3

- **Member 1 (Data Lead)**: All cleaned datasets (`master_dataset.csv`) remain completely intact. `features_dataset.csv` extends your master data with 20 leak-free lag and rolling features.
- **Member 3 (Frontend / Dashboard Lead)**:
  - Connect your UI/Dashboard directly to [`data/processed/recommendations.csv`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/data/processed/recommendations.csv) or [`data/processed/stocksense_decision_output.csv`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/data/processed/stocksense_decision_output.csv).
  - Use `Risk_Level` (`HIGH`, `MEDIUM`, `LOW`) for alert badging.
  - Use `Recommended_Order_Qty` and `Manager_Action` for prescriptive table displays.
  - Display [`reports/figures/stockout_confusion_matrix.png`](file:///Users/rupeshmacbook/Desktop/InntelliData_2026/reports/figures/stockout_confusion_matrix.png) in the ML performance tab.
