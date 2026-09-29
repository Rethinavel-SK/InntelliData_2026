# STOCKSENSE: Retail Inventory Optimization & Demand Forecasting (IntelliData 2026)

StockSense is an end-to-end AI-powered supply chain management platform designed for retail store networks in Tamil Nadu (Coimbatore, Chennai, Madurai, Salem). It performs daily demand forecasting, stock-out risk prediction, model explainability, and prescriptive inventory replenishment recommendations.

---

## 🚀 Repository Architecture & Team Deliverables

### Member 1: Data Audit, Cleaning & Master Integration
- `src/data_audit.py`: Performs non-mutating 7-point data quality audit across all raw datasets.
- `src/data_cleaning.py`: Executes deduplication, quantity filtering, category normalization, linear time-series temperature imputation, and daily store-product aggregation.
- `data/processed/master_dataset.csv`: Unified analytical master table (736 rows × 40 columns) at grain **1 Row = 1 Date × 1 Store × 1 Product**.

### Member 2: Feature Engineering, ML Forecasting, Risk & Recommendations
- `src/feature_engineering.py`: Computes 20 leak-free time, lag, rolling, inventory, and price features + 7-day target.
- `src/demand_forecasting.py`: Benchmarks 7 regression models on 7-day future demand. Best model: **Random Forest Regressor** ($MAE = 17.36$, $R^2 = 0.9947$).
- `src/stockout_prediction.py`: Benchmarks 7 classification models on stock-out risk. Best model: **Decision Tree Classifier** ($Accuracy = 96.25\%$, $Recall = 100\%$).
- `src/explainability.py`: Extracts feature drivers and generates store-product explanation reasons.
- `src/recommendation_engine.py`: Computes safety stock buffers, recommended order quantities, and manager action alerts.
- `reports/member2_summary.md`: Detailed validation report and model benchmarking results.

---

## 🛠 Project Structure

```
InntelliData_2026/
├── data/
│   ├── raw/                           # Raw POS, Inventory, Stores, Products & Weather CSVs
│   └── processed/                     # Processed datasets & ML decision tables
│       ├── master_dataset.csv         # Consolidated analytical table (736 rows x 40 cols)
│       ├── features_dataset.csv       # Feature matrix with lags & rolling stats (400 rows x 60 cols)
│       ├── recommendations.csv        # Actionable replenishment decision table
│       └── stocksense_decision_output.csv # Complete integrated decision output dataset
├── src/                               # Python modules
│   ├── data_audit.py                  # Data quality audit script (Member 1)
│   ├── data_cleaning.py               # Data cleaning & master dataset creation (Member 1)
│   ├── feature_engineering.py         # Feature engineering & target creation (Member 2)
│   ├── demand_forecasting.py          # 7-day demand forecasting pipeline (Member 2)
│   ├── stockout_prediction.py         # Stock-out risk classification pipeline (Member 2)
│   ├── explainability.py              # Model explainability & reason engine (Member 2)
│   └── recommendation_engine.py       # Inventory recommendation engine (Member 2)
├── models/                            # Serialized ML models
│   ├── demand_forecast_model.joblib   # Trained Random Forest Regressor
│   └── stockout_prediction_model.joblib # Trained Decision Tree Classifier
├── reports/                           # Audit, benchmark & explainability reports
│   ├── data_quality_report.csv
│   ├── data_cleaning_report.csv
│   ├── feature_dictionary.md
│   ├── demand_model_comparison.csv
│   ├── demand_feature_importance.csv
│   ├── stockout_model_comparison.csv
│   ├── stockout_feature_importance.csv
│   ├── explainability_summary.csv
│   ├── explainability_summary.md
│   ├── member2_summary.md
│   └── figures/
│       └── stockout_confusion_matrix.png
├── requirements.txt                   # Dependency file
└── .gitignore                         # Git ignore rules
```

---

## 💻 How to Run the Pipeline

### 1. Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Data Pipeline (Member 1)
```bash
python3 src/data_audit.py
python3 src/data_cleaning.py
```

### 3. Run ML & Decision Engine (Member 2)
```bash
python3 src/feature_engineering.py
python3 src/demand_forecasting.py
python3 src/stockout_prediction.py
python3 src/explainability.py
python3 src/recommendation_engine.py
```

---

## 📊 Key Results

- **7-Day Demand Forecasting**: **Random Forest Regressor** achieved **MAE 17.36 units**, **MAPE 3.08%**, **R² 0.9947**.
- **Stock-out Risk Classification**: **Decision Tree Classifier** achieved **Accuracy 96.25%**, **Recall 100.0%**, **F1-Score 0.9771**, **ROC-AUC 0.9062**.
- **Top Feature Drivers**: `inventory_to_demand_ratio` (0.8172), `days_of_inventory` (0.0683), `opening` (0.0467), `reorder_lvl` (0.0305).
