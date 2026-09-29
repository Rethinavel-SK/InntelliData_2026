"""
STOCKSENSE - NovaMart Inventory Decision Support Dashboard
===========================================================
StockSense Round 3 - Interactive Streamlit Prototype

Built for retail store inventory management, demand forecasting visualization,
stockout risk monitoring, model explainability, and prescriptive reorder recommendations.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

import utils

# -------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -------------------------------------------------------------
st.set_page_config(
    page_title="STOCKSENSE – NovaMart Inventory Decision Support",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject modern CSS
st.markdown(utils.get_custom_css(), unsafe_allow_html=True)

# -------------------------------------------------------------
# LOAD DATASETS
# -------------------------------------------------------------
rec_df = utils.load_recommendations()
dec_df = utils.load_decision_output()
master_df = utils.load_master_dataset()
demand_comp_df = utils.load_demand_model_comparison()
stockout_comp_df = utils.load_stockout_model_comparison()
feature_imp_df = utils.load_stockout_feature_importance()
explain_df = utils.load_explainability_summary()

if rec_df.empty:
    st.error("Error: Recommendations dataset could not be loaded. Please run the pipeline first.")
    st.stop()

# -------------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/000000/box-moving.png", width=70)
st.sidebar.title("STOCKSENSE Control")
st.sidebar.markdown("**NovaMart Inventory Operations**")
st.sidebar.markdown("---")

# Filter 1: Date Range / Single Date
available_dates = sorted(rec_df["date"].unique(), reverse=True)
selected_date = st.sidebar.selectbox("📅 Select Date", options=["All Dates", "Latest Date (" + available_dates[0] + ")"] + available_dates)

# Filter 2: Store
available_stores = sorted(rec_df["Store"].unique())
selected_stores = st.sidebar.multiselect("🏪 Filter Store(s)", options=available_stores, default=available_stores)

# Filter 3: Category
available_categories = sorted(rec_df["Category"].unique())
selected_categories = st.sidebar.multiselect("🏷️ Filter Category", options=available_categories, default=available_categories)

# Filter 4: Risk Level
available_risks = ["HIGH", "MEDIUM", "LOW"]
selected_risks = st.sidebar.multiselect("⚠️ Risk Level Filter", options=available_risks, default=available_risks)

# Apply filters to recommendations and decision dataframes
filtered_rec = rec_df.copy()
filtered_dec = dec_df.copy()

if selected_date == "Latest Date (" + available_dates[0] + ")":
    filtered_rec = filtered_rec[filtered_rec["date"] == available_dates[0]]
    filtered_dec = filtered_dec[filtered_dec["date"] == available_dates[0]]
elif selected_date != "All Dates":
    filtered_rec = filtered_rec[filtered_rec["date"] == selected_date]
    filtered_dec = filtered_dec[filtered_dec["date"] == selected_date]

if selected_stores:
    filtered_rec = filtered_rec[filtered_rec["Store"].isin(selected_stores)]
    if "store_id" in filtered_dec.columns:
        filtered_dec = filtered_dec[filtered_dec["store_id"].isin(selected_stores)]

if selected_categories:
    filtered_rec = filtered_rec[filtered_rec["Category"].isin(selected_categories)]
    if "category" in filtered_dec.columns:
        filtered_dec = filtered_dec[filtered_dec["category"].isin(selected_categories)]

if selected_risks:
    filtered_rec = filtered_rec[filtered_rec["Risk_Level"].isin(selected_risks)]

st.sidebar.markdown("---")
st.sidebar.info(f"Showing **{len(filtered_rec)}** product-store records matching active filters.")

# -------------------------------------------------------------
# MAIN DASHBOARD HEADER
# -------------------------------------------------------------
st.title("📦 STOCKSENSE – NovaMart Inventory Decision Support")
st.markdown("##### *AI-Powered Demand Forecasting, Stock-out Prevention & Prescriptive Inventory Replenishment*")
st.markdown("---")

# -------------------------------------------------------------
# TABS NAVIGATION
# -------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Executive Summary",
    "⚠️ Inventory Risk Centre",
    "⚡ Manager Action Centre",
    "📈 Demand Intelligence",
    "🔬 Model Performance",
    "💡 Model Explainability"
])

# =============================================================
# TAB 1: EXECUTIVE SUMMARY
# =============================================================
with tab1:
    st.subheader("Operational Overview & Key Performance Indicators")
    
    # Calculate KPIs
    if not filtered_dec.empty:
        total_rev = filtered_dec["tx_total_revenue"].sum() if "tx_total_revenue" in filtered_dec.columns else 0.0
        total_units = filtered_dec["daily_demand"].sum() if "daily_demand" in filtered_dec.columns else 0
        stockout_count = (filtered_dec["closing"] == 0).sum() if "closing" in filtered_dec.columns else 0
        stockout_rate = (stockout_count / len(filtered_dec) * 100.0) if len(filtered_dec) > 0 else 0.0
    else:
        total_rev, total_units, stockout_rate = 0.0, 0, 0.0

    high_risk_count = (filtered_rec["Risk_Level"] == "HIGH").sum()
    reorder_count = (filtered_rec["Recommended_Order_Qty"] > 0).sum()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">{utils.format_currency(total_rev)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Demand (Units)</div>
            <div class="metric-value">{total_units:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Stockout Rate</div>
            <div class="metric-value">{stockout_rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High Risk Products</div>
            <div class="metric-value" style="color:#ef4444;">{high_risk_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Reorders Needed</div>
            <div class="metric-value" style="color:#f59e0b;">{reorder_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 🏬 Demand & Revenue by Store")
        if not filtered_dec.empty and "store_id" in filtered_dec.columns:
            store_agg = filtered_dec.groupby("store_id").agg(
                Revenue=("tx_total_revenue", "sum"),
                Demand=("daily_demand", "sum")
            ).reset_index()

            fig_store = px.bar(
                store_agg, x="store_id", y="Revenue",
                color="store_id", text_auto=".2s",
                labels={"store_id": "Store ID", "Revenue": "Total Revenue (₹)"},
                title="Revenue Contribution by Store Location",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_store.update_layout(template="plotly_dark", height=380)
            st.plotly_chart(fig_store, use_container_width=True)

    with c2:
        st.markdown("### 🎯 Inventory Stock-out Risk Distribution")
        risk_counts = filtered_rec["Risk_Level"].value_counts().reset_index()
        risk_counts.columns = ["Risk_Level", "Count"]

        fig_risk = px.pie(
            risk_counts, values="Count", names="Risk_Level",
            color="Risk_Level",
            color_discrete_map={"HIGH": "#ef4444", "MEDIUM": "#f59e0b", "LOW": "#10b981"},
            hole=0.4,
            title="Proportion of Products by Risk Level"
        )
        fig_risk.update_layout(template="plotly_dark", height=380)
        st.plotly_chart(fig_risk, use_container_width=True)

# =============================================================
# TAB 2: INVENTORY RISK CENTRE
# =============================================================
with tab2:
    st.subheader("⚠️ Inventory Risk Center & Replenishment Monitor")
    st.markdown("Filter and inspect real-time inventory risk across stores, categories, and risk levels.")

    # Highlighting helper
    def color_risk(val):
        if val == "HIGH":
            return "background-color: #7f1d1d; color: white; font-weight: bold;"
        elif val == "MEDIUM":
            return "background-color: #78350f; color: white; font-weight: bold;"
        else:
            return "background-color: #064e3b; color: white; font-weight: bold;"

    display_cols = [
        "date", "Store", "Product", "Category", "Current_Stock", "7_Day_Forecast",
        "Stockout_Probability", "Risk_Level", "Recommended_Order_Qty"
    ]
    disp_df = filtered_rec[[c for c in display_cols if c in filtered_rec.columns]].copy()
    
    if "Stockout_Probability" in disp_df.columns:
        disp_df["Stockout_Probability"] = (disp_df["Stockout_Probability"] * 100.0).round(1).astype(str) + "%"

    st.dataframe(
        disp_df.style.applymap(color_risk, subset=["Risk_Level"]),
        use_container_width=True,
        height=450
    )

    # Export CSV
    csv_bytes = disp_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Risk Table (CSV)",
        data=csv_bytes,
        file_name="stocksense_inventory_risk_report.csv",
        mime="text/csv"
    )

# =============================================================
# TAB 3: MANAGER ACTION CENTRE (Prescriptive Recommendations)
# =============================================================
with tab3:
    st.subheader("⚡ Manager Action Centre – Prescriptive Inventory Orders")
    st.markdown("Actionable purchase order recommendations prioritized by critical stock-out risk.")

    high_risk_items = filtered_rec[filtered_rec["Risk_Level"] == "HIGH"].sort_values("Recommended_Order_Qty", ascending=False)
    other_items = filtered_rec[filtered_rec["Risk_Level"] != "HIGH"].sort_values("Recommended_Order_Qty", ascending=False)

    total_recommendations = pd.concat([high_risk_items, other_items]).reset_index(drop=True)

    if total_recommendations.empty:
        st.success("🎉 No products currently require reordering under active filters!")
    else:
        st.markdown(f"Displaying **{len(total_recommendations)}** purchase recommendations:")
        
        for idx, row in total_recommendations.head(15).iterrows():
            risk_color = "#ef4444" if row["Risk_Level"] == "HIGH" else ("#f59e0b" if row["Risk_Level"] == "MEDIUM" else "#10b981")
            prob_pct = f"{float(row['Stockout_Probability']) * 100.0:.1f}%"

            header_text = f"🏪 Store {row['Store']} | SKU {row['Product']} ({row['Category']} - {row['Brand']}) — Risk: {row['Risk_Level']}"

            with st.expander(header_text, expanded=(idx < 3)):
                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("Predicted 7-Day Demand", f"{int(row['7_Day_Forecast']):,} units")
                with rc2:
                    st.metric("Current Stock (Closing)", f"{int(row['Current_Stock'])} units")
                with rc3:
                    st.metric("Stock-out Probability", prob_pct)
                with rc4:
                    st.metric("Recommended Order Qty", f"{int(row['Recommended_Order_Qty']):,} units")

                st.markdown(f"""
                <div class="action-box" style="border-left-color: {risk_color};">
                    <strong style="color:{risk_color}; font-size:1.1rem;">📋 MANAGER ACTION:</strong><br>
                    <span style="font-size:1.05rem; color:#f8fafc;">{row['Manager_Action']}</span><br><br>
                    <strong>💡 Key Drivers / Root Cause:</strong><br>
                    <span style="color:#cbd5e1;">{row['Key_Reasons']}</span>
                </div>
                """, unsafe_allow_html=True)

# =============================================================
# TAB 4: DEMAND INTELLIGENCE
# =============================================================
with tab4:
    st.subheader("📈 Demand Intelligence & Trend Analysis")

    if not master_df.empty:
        m_df = master_df.copy()
        if selected_stores:
            m_df = m_df[m_df["store_id"].isin(selected_stores)]
        if selected_categories:
            m_df = m_df[m_df["category"].isin(selected_categories)]

        st.markdown("### 📅 Daily Demand Trend by Store")
        daily_trend = m_df.groupby(["date", "store_id"])["daily_demand"].sum().reset_index()

        fig_line = px.line(
            daily_trend, x="date", y="daily_demand", color="store_id",
            markers=True,
            title="Daily POS Units Sold over Time per Store Location",
            labels={"date": "Date", "daily_demand": "Daily Demand (Units)", "store_id": "Store"}
        )
        fig_line.update_layout(template="plotly_dark", height=420)
        st.plotly_chart(fig_line, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🏷️ Category Demand Distribution")
            cat_demand = m_df.groupby("category")["daily_demand"].sum().reset_index()
            fig_cat = px.bar(
                cat_demand, x="category", y="daily_demand", color="category",
                text_auto=True,
                title="Total Demand Units Sold by Product Category",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_cat.update_layout(template="plotly_dark", height=360)
            st.plotly_chart(fig_cat, use_container_width=True)

        with c2:
            st.markdown("### ☀️ Temperature vs Demand Correlation")
            fig_scatter = px.scatter(
                m_df, x="temp_c", y="daily_demand", color="category",
                hover_data=["store_id", "product_id"],
                title="Daily Demand vs Local Temperature (°C)"
            )
            fig_scatter.update_layout(template="plotly_dark", height=360)
            st.plotly_chart(fig_scatter, use_container_width=True)

# =============================================================
# TAB 5: MODEL PERFORMANCE
# =============================================================
with tab5:
    st.subheader("🔬 Machine Learning Model Benchmarking & Accuracy")

    st.markdown("""
    <div style="background-color:#0f172a; padding:16px; border-radius:8px; border:1px solid #334155; margin-bottom:20px;">
        <h4 style="color:#38bdf8; margin:0;">🏆 Champion Production Models</h4>
        <ul>
            <li><strong>7-Day Demand Forecasting:</strong> <span style="color:#10b981; font-weight:bold;">Random Forest Regressor</span> (MAE: 17.36 units, MAPE: 3.08%, R²: 0.9947)</li>
            <li><strong>Stock-out Classification:</strong> <span style="color:#10b981; font-weight:bold;">Decision Tree Classifier</span> (Accuracy: 96.25%, Recall: 100.0%, F1: 0.9771)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown("### 📈 7-Day Demand Forecasting Models")
        if not demand_comp_df.empty:
            st.dataframe(demand_comp_df, use_container_width=True)

    with col_m2:
        st.markdown("### ⚠️ Stock-out Classification Models")
        if not stockout_comp_df.empty:
            st.dataframe(stockout_comp_df, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📊 Confusion Matrix Heatmap (Stock-out Risk Classifier)")
    
    root = utils.get_project_root()
    cm_path = root / "reports" / "figures" / "stockout_confusion_matrix.png"
    if cm_path.exists():
        st.image(str(cm_path), caption="Decision Tree Stock-out Confusion Matrix (Test Set Validation)", width=550)
    else:
        st.info("Confusion matrix plot is being generated.")

# =============================================================
# TAB 6: MODEL EXPLAINABILITY
# =============================================================
with tab6:
    st.subheader("💡 Model Explainability & Key Feature Drivers")
    st.markdown("Understanding global model decisions and store-level stockout triggers.")

    if not feature_imp_df.empty:
        st.markdown("### 🌐 Global Feature Importance (Stock-out Model)")
        top_imp = feature_imp_df.head(10)
        fig_imp = px.bar(
            top_imp, x="importance", y="feature", orientation="h",
            color="importance",
            title="Top 10 Feature Drivers of Stock-out Risk Classification",
            color_continuous_scale="Blues"
        )
        fig_imp.update_layout(template="plotly_dark", height=380, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🔍 Store x Product Root Cause Inspection")

    if not explain_df.empty:
        selected_exp_store = st.selectbox("Select Store ID for Deep-Dive", options=sorted(explain_df["store_id"].unique()))
        exp_store_df = explain_df[explain_df["store_id"] == selected_exp_store]

        for _, r in exp_store_df.head(8).iterrows():
            st.markdown(f"**Store `{r['store_id']}` | SKU `{r['product_id']}` ({r.get('category', '')})**")
            st.write(f"• Closing Stock: **{int(r['closing'])}** | Reorder Level: **{int(r['reorder_lvl'])}** | Days of Supply: **{r.get('days_of_inventory', 0):.1f} days**")
            st.info(f"Key Reasons: {r['explanation_reasons']}")

# -------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #94a3b8; font-size: 0.9rem; padding: 10px;">
        STOCKSENSE © 2026 | <strong>IntelliData 2026 Hackathon</strong> | <em>Sri Eshwar College of Engineering</em>
    </div>
    """,
    unsafe_allow_html=True
)
