"""
STOCKSENSE - NovaMart Inventory Decision Support Dashboard
===========================================================
StockSense Round 3 - Cronza Webflow Aesthetic Prototype

Designed with the Cronza dark-mode glassmorphism design system.
Integrates 7-day demand forecasting, stockout risk prediction,
model explainability, and prescriptive inventory reorder recommendations.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import utils

# -------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(
    page_title="STOCKSENSE – NovaMart Inventory Decision Support",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Cronza Webflow CSS Design System
st.markdown(utils.get_cronza_css(), unsafe_allow_html=True)

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
# SIDEBAR FILTERS (CRONZA STYLED)
# -------------------------------------------------------------
st.sidebar.markdown('<div class="cronza-pill">⚡ STOCKSENSE ENGINE 3.0</div>', unsafe_allow_html=True)
st.sidebar.title("Control Centre")
st.sidebar.markdown("*NovaMart Retail Operations*")
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

# Filter Logic
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
st.sidebar.info(f"Active Filter Records: **{len(filtered_rec)}** SKUs")

# -------------------------------------------------------------
# CRONZA HERO HEADER
# -------------------------------------------------------------
st.markdown('<div class="cronza-pill">✨ INTELLIDATA 2026 • ROUND 3 PROTOTYPE</div>', unsafe_allow_html=True)
st.markdown('<div class="cronza-title">STOCKSENSE – NovaMart Inventory Decision Support</div>', unsafe_allow_html=True)
st.markdown('<div class="cronza-subtitle">AI-driven 7-day demand forecasting, automated stockout risk classification & prescriptive replenishment engine.</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# DASHBOARD TABS
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
    st.markdown("### 📊 Operational Overview & KPI Summary")
    
    if not filtered_dec.empty:
        total_rev = filtered_dec["tx_total_revenue"].sum() if "tx_total_revenue" in filtered_dec.columns else 0.0
        total_units = filtered_dec["daily_demand"].sum() if "daily_demand" in filtered_dec.columns else 0
        stockout_count = (filtered_dec["closing"] == 0).sum() if "closing" in filtered_dec.columns else 0
        stockout_rate = (stockout_count / len(filtered_dec) * 100.0) if len(filtered_dec) > 0 else 0.0
    else:
        total_rev, total_units, stockout_rate = 0.0, 0, 0.0

    high_risk_count = (filtered_rec["Risk_Level"] == "HIGH").sum()
    reorder_count = (filtered_rec["Recommended_Order_Qty"] > 0).sum()

    kcol1, kcol2, kcol3, kcol4, kcol5 = st.columns(5)

    with kcol1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">{utils.format_currency(total_rev)}</div>
        </div>
        """, unsafe_allow_html=True)

    with kcol2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Demand</div>
            <div class="metric-value">{total_units:,} <span style="font-size:0.9rem; color:#94a3b8;">units</span></div>
        </div>
        """, unsafe_allow_html=True)

    with kcol3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Stockout Rate</div>
            <div class="metric-value" style="color:{'#f43f5e' if stockout_rate > 5 else '#10b981'};">{stockout_rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with kcol4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High Risk SKUs</div>
            <div class="metric-value" style="color:#f43f5e;">{high_risk_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with kcol5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Reorders Needed</div>
            <div class="metric-value" style="color:#f59e0b;">{reorder_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 🏬 Revenue Contribution by Store")
        if not filtered_dec.empty and "store_id" in filtered_dec.columns:
            store_agg = filtered_dec.groupby("store_id").agg(
                Revenue=("tx_total_revenue", "sum"),
                Demand=("daily_demand", "sum")
            ).reset_index()

            fig_store = px.bar(
                store_agg, x="store_id", y="Revenue",
                color="store_id", text_auto=".2s",
                labels={"store_id": "Store Location", "Revenue": "Total Revenue (₹)"},
                color_discrete_sequence=["#818cf8", "#38bdf8", "#34d399", "#fbbf24"]
            )
            fig_store.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc", family="Plus Jakarta Sans"),
                height=360
            )
            st.plotly_chart(fig_store, use_container_width=True)

    with c2:
        st.markdown("#### 🎯 Inventory Stock-out Risk Distribution")
        risk_counts = filtered_rec["Risk_Level"].value_counts().reset_index()
        risk_counts.columns = ["Risk_Level", "Count"]

        fig_risk = px.pie(
            risk_counts, values="Count", names="Risk_Level",
            color="Risk_Level",
            color_discrete_map={"HIGH": "#f43f5e", "MEDIUM": "#f59e0b", "LOW": "#10b981"},
            hole=0.5
        )
        fig_risk.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc", family="Plus Jakarta Sans"),
            height=360
        )
        st.plotly_chart(fig_risk, use_container_width=True)

# =============================================================
# TAB 2: INVENTORY RISK CENTRE
# =============================================================
with tab2:
    st.markdown("### ⚠️ Inventory Risk Center & Monitoring")
    st.markdown("Filter and inspect real-time stock-out risks across all retail stores and categories.")

    def apply_risk_badge_style(val):
        if val == "HIGH":
            return "background-color: rgba(244, 63, 94, 0.2); color: #fecdd3; font-weight: bold; border: 1px solid rgba(244, 63, 94, 0.5);"
        elif val == "MEDIUM":
            return "background-color: rgba(245, 158, 11, 0.2); color: #fde68a; font-weight: bold; border: 1px solid rgba(245, 158, 11, 0.5);"
        else:
            return "background-color: rgba(16, 185, 129, 0.2); color: #a7f3d0; font-weight: bold; border: 1px solid rgba(16, 185, 129, 0.5);"

    display_cols = [
        "date", "Store", "Product", "Category", "Current_Stock", "7_Day_Forecast",
        "Stockout_Probability", "Risk_Level", "Recommended_Order_Qty"
    ]
    disp_df = filtered_rec[[c for c in display_cols if c in filtered_rec.columns]].copy()
    
    if "Stockout_Probability" in disp_df.columns:
        disp_df["Stockout_Probability"] = (disp_df["Stockout_Probability"] * 100.0).round(1).astype(str) + "%"

    st.dataframe(
        disp_df.style.applymap(apply_risk_badge_style, subset=["Risk_Level"]),
        use_container_width=True,
        height=450
    )

    csv_bytes = disp_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Export Risk Data Report (CSV)",
        data=csv_bytes,
        file_name="stocksense_inventory_risk_report.csv",
        mime="text/csv"
    )

# =============================================================
# TAB 3: MANAGER ACTION CENTRE (CRONZA GLASS CARDS)
# =============================================================
with tab3:
    st.markdown("### ⚡ Manager Action Centre – Prescriptive Order Recommendations")
    st.markdown("Automated stock replenishment orders prioritized by business urgency.")

    high_risk_items = filtered_rec[filtered_rec["Risk_Level"] == "HIGH"].sort_values("Recommended_Order_Qty", ascending=False)
    other_items = filtered_rec[filtered_rec["Risk_Level"] != "HIGH"].sort_values("Recommended_Order_Qty", ascending=False)

    total_recommendations = pd.concat([high_risk_items, other_items]).reset_index(drop=True)

    if total_recommendations.empty:
        st.success("🎉 No products currently require reordering under active filters.")
    else:
        for idx, row in total_recommendations.head(15).iterrows():
            risk_color = "#f43f5e" if row["Risk_Level"] == "HIGH" else ("#f59e0b" if row["Risk_Level"] == "MEDIUM" else "#10b981")
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
                    st.metric("Recommended Reorder Qty", f"{int(row['Recommended_Order_Qty']):,} units")

                st.markdown(f"""
                <div class="cronza-action-card" style="border-left-color: {risk_color};">
                    <div style="color:{risk_color}; font-weight:800; font-size:1.1rem; margin-bottom:6px;">📋 PRESCRIPTIVE MANAGER ACTION:</div>
                    <div style="font-size:1.05rem; color:#f8fafc; font-weight:600; margin-bottom:12px;">{row['Manager_Action']}</div>
                    <div style="color:#94a3b8; font-weight:700; font-size:0.85rem; text-transform:uppercase;">💡 Key Driver & Root Cause:</div>
                    <div style="color:#cbd5e1; font-size:0.95rem;">{row['Key_Reasons']}</div>
                </div>
                """, unsafe_allow_html=True)

# =============================================================
# TAB 4: DEMAND INTELLIGENCE
# =============================================================
with tab4:
    st.markdown("### 📈 Demand Intelligence & Time-Series Dynamics")

    if not master_df.empty:
        m_df = master_df.copy()
        if selected_stores:
            m_df = m_df[m_df["store_id"].isin(selected_stores)]
        if selected_categories:
            m_df = m_df[m_df["category"].isin(selected_categories)]

        st.markdown("#### 📅 Daily Store Demand History & Forecast Horizon")
        daily_trend = m_df.groupby(["date", "store_id"])["daily_demand"].sum().reset_index()

        fig_line = px.line(
            daily_trend, x="date", y="daily_demand", color="store_id",
            markers=True,
            labels={"date": "Date", "daily_demand": "POS Demand (Units)", "store_id": "Store Location"},
            color_discrete_sequence=["#818cf8", "#38bdf8", "#34d399", "#fbbf24"]
        )
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc", family="Plus Jakarta Sans"),
            height=420
        )
        st.plotly_chart(fig_line, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🏷️ Demand by Product Category")
            cat_demand = m_df.groupby("category")["daily_demand"].sum().reset_index()
            fig_cat = px.bar(
                cat_demand, x="category", y="daily_demand", color="category",
                text_auto=True,
                color_discrete_sequence=["#a7f3d0", "#bae6fd", "#c7d2fe", "#fde68a"]
            )
            fig_cat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc", family="Plus Jakarta Sans"),
                height=360
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        with c2:
            st.markdown("#### ☀️ Local Temperature vs Demand Correlation")
            fig_scatter = px.scatter(
                m_df, x="temp_c", y="daily_demand", color="category",
                hover_data=["store_id", "product_id"],
                labels={"temp_c": "Temperature (°C)", "daily_demand": "Daily Demand"}
            )
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc", family="Plus Jakarta Sans"),
                height=360
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

# =============================================================
# TAB 5: MODEL PERFORMANCE
# =============================================================
with tab5:
    st.markdown("### 🔬 Production Machine Learning Benchmark")

    st.markdown("""
    <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(165, 180, 252, 0.3); padding: 20px; border-radius: 16px; margin-bottom: 24px;">
        <h4 style="color:#a5b4fc; margin-top:0;">🏆 Selected Production Champion Models</h4>
        <div style="display:flex; gap:30px; margin-top:10px;">
            <div>
                <strong style="color:#ffffff;">1. Demand Forecasting Regressor:</strong><br>
                <span style="color:#10b981; font-weight:bold;">Random Forest Regressor</span> (MAE: 17.36 units | MAPE: 3.08% | R²: 0.9947)
            </div>
            <div>
                <strong style="color:#ffffff;">2. Stock-out Risk Classifier:</strong><br>
                <span style="color:#10b981; font-weight:bold;">Decision Tree Classifier</span> (Accuracy: 96.25% | Recall: 100.0% | F1: 0.9771)
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown("#### 📈 7-Day Demand Regression Models")
        if not demand_comp_df.empty:
            st.dataframe(demand_comp_df, use_container_width=True)

    with col_m2:
        st.markdown("#### ⚠️ Stock-out Classification Models")
        if not stockout_comp_df.empty:
            st.dataframe(stockout_comp_df, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📊 Stock-out Risk Classifier Confusion Matrix")
    
    root = utils.get_project_root()
    cm_path = root / "reports" / "figures" / "stockout_confusion_matrix.png"
    if cm_path.exists():
        st.image(str(cm_path), caption="Decision Tree Classifier Confusion Matrix (Test Validation Set)", width=520)

# =============================================================
# TAB 6: MODEL EXPLAINABILITY
# =============================================================
with tab6:
    st.markdown("### 💡 Model Explainability & Global Feature Importance")

    if not feature_imp_df.empty:
        top_imp = feature_imp_df.head(10)
        fig_imp = px.bar(
            top_imp, x="importance", y="feature", orientation="h",
            color="importance",
            title="Top Feature Drivers of Stock-out Risk",
            color_continuous_scale="Purples"
        )
        fig_imp.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc", family="Plus Jakarta Sans"),
            height=380,
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🔍 Store SKU Root Cause Inspection")

    if not explain_df.empty:
        selected_exp_store = st.selectbox("Select Store ID for Deep-Dive", options=sorted(explain_df["store_id"].unique()))
        exp_store_df = explain_df[explain_df["store_id"] == selected_exp_store]

        for _, r in exp_store_df.head(8).iterrows():
            st.markdown(f"**Store `{r['store_id']}` | SKU `{r['product_id']}` ({r.get('category', '')})**")
            st.write(f"• Closing Stock: **{int(r['closing'])}** | Reorder Level: **{int(r['reorder_lvl'])}** | Supply Coverage: **{r.get('days_of_inventory', 0):.1f} days**")
            st.info(f"Root Cause Analysis: {r['explanation_reasons']}")

# -------------------------------------------------------------
# CRONZA FOOTER
# -------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 20px 0;">
        ⚡ <strong>STOCKSENSE 3.0</strong> • Built with Cronza Webflow Aesthetic System<br>
        <em>IntelliData 2026 Hackathon | Sri Eshwar College of Engineering</em>
    </div>
    """,
    unsafe_allow_html=True
)
