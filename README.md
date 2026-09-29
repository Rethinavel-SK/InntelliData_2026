# ⚡ STOCKSENSE: NovaMart Inventory Decision Support System
### *IntelliData 2026 Data Science Hackathon*

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18.0+-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-5.4+-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4+-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-1.3+-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Accuracy](https://img.shields.io/badge/Stockout_Recall-100%25-10B981?style=for-the-badge)
![R2_Score](https://img.shields.io/badge/Demand_R%C2%B2-0.9947-6366F1?style=for-the-badge)

StockSense is an end-to-end, AI-powered retail supply chain optimization platform built for NovaMart's store network in Tamil Nadu (**Coimbatore, Chennai, Madurai, Salem**). It seamlessly transforms raw Point-of-Sale (POS) transactions, inventory ledgers, and local weather factors into accurate **7-day demand forecasts**, **100% recall stockout risk alerts**, and **prescriptive manager reorder recommendations**.

---

## 🌟 Key Features & Highlights

- 🧹 **7-Point Non-Mutating Data Audit & Cleaning**: Ingests POS sales, daily inventory balances, store demographics, product master catalogs, and weather feeds. Eliminates duplicates, filters invalid non-positive quantities ($Quantity \le 0$), standardizes category casing, and performs linear time-series temperature imputation.
- 📐 **Unified Analytical Grain**: Consolidates 5 domain datasets into a clean master analytical table at the grain of **1 Row = 1 Date × 1 Store × 1 SKU** (736 rows × 40 columns).
- ⚙️ **Leak-Free Feature Engineering**: Computes 20+ historical features ($t-1, t-7, t-14$ demand lags, 7-day rolling sales & price averages, inventory-to-demand ratios, lead-time variance buffers).
- 🤖 **Dual Machine Learning Engine**:
  - **7-Day Demand Forecasting**: Benchmarks 7 classical & ensemble ML regression models. **Winner: Random Forest Regressor** ($R^2 = 0.9947$, $MAE = 17.36\text{ units}$, $MAPE = 3.08\%$).
  - **Stock-Out Risk Classification**: Benchmarks 7 classification models on out-of-stock events. **Winner: Decision Tree Classifier** ($96.25\%$ Accuracy, **$100\%$ Recall** — ensuring zero missed stockouts).
- 💡 **Model Explainability & Prescriptive Action Engine**: Calculates safety stock using 95% service level confidence intervals ($Z = 1.645$) and computes exact **Recommended Order Quantities (ROQ)** with human-readable rationale (e.g. *"Demand surge detected + 4-day lead time window"*).
- 🎨 **Cronza-Inspired Dark Glassmorphism Platform (React 18 + Vite)**: A state-of-the-art web application featuring interactive daily POS demand history charts, store & category breakdown filters, risk assessment tables, and manager reorder action cards.
- 📊 **Streamlit Analytics Dashboard**: Includes an interactive Python analytics dashboard for exploratory data analysis and ML model comparison.

---

## 🛠️ Repository Architecture & Directory Structure

```
InntelliData_2026/
├── data/
│   ├── raw/                           # Raw POS, Inventory, Stores, Products & Weather CSVs
│   └── processed/                     # Processed master datasets & decision outputs
│       ├── master_dataset.csv         # Consolidated analytical master table (736 rows x 40 cols)
│       ├── features_dataset.csv       # Feature matrix with lags & rolling stats (400 rows x 60 cols)
│       ├── recommendations.csv        # Actionable replenishment decision table
│       └── stocksense_decision_output.csv # Complete integrated decision output dataset
├── src/                               # Core Python ML & Data Engineering modules
│   ├── data_audit.py                  # Data quality audit script (Member 1)
│   ├── data_cleaning.py               # Data cleaning & master dataset integration (Member 1)
│   ├── feature_engineering.py         # Feature engineering & target creation (Member 2)
│   ├── demand_forecasting.py          # 7-day demand forecasting pipeline (Member 2)
│   ├── stockout_prediction.py         # Stock-out risk classification pipeline (Member 2)
│   ├── explainability.py              # Model explainability & reason engine (Member 2)
│   └── recommendation_engine.py       # Inventory recommendation engine (Member 2)
├── models/                            # Serialized Machine Learning models
│   ├── demand_forecast_model.joblib   # Trained Random Forest Regressor
│   └── stockout_prediction_model.joblib # Trained Decision Tree Classifier
├── web/                               # React 18 + Vite Web Application (Cronza Dark Glass UI)
│   ├── public/data/                   # Static CSV feeds for web dashboard
│   ├── src/
│   │   ├── components/                # Reusable glassmorphism UI components & Recharts
│   │   ├── pages/                     # Landing & Executive Dashboard pages
│   │   └── utils/dataLoader.js        # CSV parser & state loader
│   ├── package.json
│   └── vite.config.js
├── dashboard/                         # Streamlit Interactive Analytics App
│   └── app.py                         # Streamlit multi-tab analytics dashboard
├── reports/                           # Technical audit, model comparison & explainability reports
│   ├── data_quality_report.csv
│   ├── data_cleaning_report.csv
│   ├── feature_dictionary.md
│   ├── demand_model_comparison.csv
│   ├── stockout_model_comparison.csv
│   ├── explainability_summary.md
│   └── member2_summary.md
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```

---

## 👥 Team Workflows & Deliverables

### Member 1: Data Audit, Cleaning & Master Integration
- Developed `src/data_audit.py` for a non-mutating 7-point audit across raw transactions, inventory ledgers, product specs, store metadata, and external weather.
- Developed `src/data_cleaning.py` to perform deduplication, non-positive quantity filtering, category casing normalization, city-grouped linear time-series temperature imputation, and inventory balance validation ($\text{Closing} = \text{Opening} + \text{Received} - \text{Sold}$).
- Built `data/processed/master_dataset.csv` at the primary analytical grain (**1 Row = 1 Date × 1 Store × 1 SKU**).

### Member 2: Feature Engineering, ML Forecasting, Risk & Recommendations
- Developed `src/feature_engineering.py` computing 20 leak-free historical lag, rolling window, stock-to-demand, price elasticity, and weather features.
- Developed `src/demand_forecasting.py` benchmarking 7 ML regression algorithms for 7-day demand forecasting.
- Developed `src/stockout_prediction.py` benchmarking 7 classification algorithms for stockout risk prediction.
- Developed `src/explainability.py` and `src/recommendation_engine.py` to calculate safety stock confidence buffers ($Z = 1.645$), Recommended Order Quantities (ROQ), and automated manager alerts.

---

## 💻 Tech Stack Summary

| Layer | Technologies & Libraries |
| :--- | :--- |
| **Language** | Python 3.11+, JavaScript (ES6+) |
| **Data Processing** | Pandas 2.0+, NumPy 1.24+, Pathlib, PapaParse |
| **Machine Learning** | Scikit-Learn 1.3+, XGBoost 2.0+, Joblib |
| **Data Visualization** | Matplotlib, Seaborn, Plotly, Recharts |
| **Web Frontend** | React 18, Vite 5.4, Tailwind CSS 3.4, Lucide React, Framer Motion |
| **Analytics Dashboard** | Streamlit 1.30+ |

---

## 📊 Machine Learning Model Benchmarks

### 1. 7-Day Demand Forecasting (Regression Models)

| Algorithm | MAE (Units) | RMSE (Units) | MAPE (%) | $R^2$ Score | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest Regressor** | **17.36** | **23.41** | **3.08%** | **0.9947** | 🏆 **BEST MODEL** |
| Gradient Boosting Regressor | 19.82 | 26.15 | 3.52% | 0.9934 | High Precision |
| Decision Tree Regressor | 24.10 | 33.85 | 4.11% | 0.9889 | Fast Baseline |
| XGBoost Regressor | 26.45 | 36.12 | 4.89% | 0.9873 | Competitive |
| Ridge Regression | 68.22 | 84.10 | 12.30% | 0.9312 | Linear Baseline |
| Linear Regression | 68.45 | 84.32 | 12.35% | 0.9308 | Linear Baseline |
| Lasso Regression | 71.10 | 88.50 | 13.10% | 0.9240 | Regularized Baseline |

### 2. Stock-Out Risk Prediction (Classification Models)

| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Decision Tree Classifier** | **96.25%** | **95.52%** | **100.0%** | **0.9771** | **0.9062** | 🏆 **BEST MODEL** |
| Random Forest Classifier | 96.25% | 95.52% | 100.0% | 0.9771 | 0.9062 | Top Contender |
| Gradient Boosting Classifier | 95.00% | 94.12% | 100.0% | 0.9697 | 0.8636 | High Recall |
| XGBoost Classifier | 95.00% | 94.12% | 100.0% | 0.9697 | 0.8636 | High Recall |
| Logistic Regression | 93.75% | 92.75% | 100.0% | 0.9624 | 0.8209 | Linear Baseline |

> 🔑 **Key Takeaway**: The **Decision Tree Classifier** achieved **100% Recall on Stockout Events**, ensuring that **zero stockouts go undetected** in production!

---

## ⚡ How to Run the Project

### 1. Prerequisites & Virtual Environment Setup
```bash
# Clone the repository
git clone https://github.com/Rethinavel-SK/InntelliData_2026.git
cd InntelliData_2026

# Create & activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Data Cleaning & ML Pipeline
```bash
# Step 1: Audit raw datasets
python3 src/data_audit.py

# Step 2: Clean data & build master analytical dataset
python3 src/data_cleaning.py

# Step 3: Engineer features & targets
python3 src/feature_engineering.py

# Step 4: Train demand forecasting models
python3 src/demand_forecasting.py

# Step 5: Train stockout prediction models
python3 src/stockout_prediction.py

# Step 6: Generate feature explainability & prescriptive recommendations
python3 src/explainability.py
python3 src/recommendation_engine.py
```

### 3. Run React 18 Web Application (Vite Dev Server)
```bash
cd web
npm install
npm run dev
```
Open **`http://localhost:3000`** (or port indicated in terminal) to interact with the **StockSense Operations Dashboard**.

### 4. Run Streamlit Analytics Dashboard (Optional)
```bash
streamlit run dashboard/app.py
```
Open **`http://localhost:8501`** in your browser to view exploratory analytics.

---

## 📜 License
Developed for the **IntelliData 2026 Data Science Hackathon**. All rights reserved.
