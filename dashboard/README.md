# STOCKSENSE Interactive Streamlit Dashboard

This directory contains the Streamlit Web Application Prototype for **STOCKSENSE - NovaMart Inventory Decision Support** (IntelliData 2026 Round 3).

---

## 🚀 How to Run the Dashboard

### 1. Activate Environment & Install Dependencies
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Launch Streamlit Application
```bash
streamlit run dashboard/app.py
```

The application will open in your default browser at `http://localhost:8501`.

---

## 📊 Dashboard Modules & Tabs

1. **📊 Executive Summary**: High-level KPIs (Total Revenue, Total Demand, Stockout Rate, High Risk Count, Reorders Needed) + Revenue distribution charts.
2. **⚠️ Inventory Risk Centre**: Filterable data table with color-coded risk levels (`HIGH`, `MEDIUM`, `LOW`) and CSV export.
3. **⚡ Manager Action Centre**: Prescriptive recommendation cards with recommended order quantities, root causes (`Key_Reasons`), and manager action alerts (`Manager_Action`).
4. **📈 Demand Intelligence**: Historical & forecasted sales trends, category demand breakdowns, and weather correlations.
5. **🔬 Model Performance**: Benchmark comparison tables for 7 demand regression models and 7 stockout classification models + confusion matrix image.
6. **💡 Model Explainability**: Global feature importances + Store × Product root cause inspection.
