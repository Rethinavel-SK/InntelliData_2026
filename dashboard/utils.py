"""
Cronza-Inspired Utility & Design System Module for StockSense Dashboard
========================================================================
StockSense Round 3 - Cronza Webflow Aesthetic Design System
"""

from pathlib import Path
import pandas as pd
import streamlit as st


def get_project_root() -> Path:
    """Return project root directory."""
    return Path(__file__).resolve().parent.parent


@st.cache_data
def load_recommendations() -> pd.DataFrame:
    root = get_project_root()
    path = root / "data" / "processed" / "recommendations.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    return df


@st.cache_data
def load_decision_output() -> pd.DataFrame:
    root = get_project_root()
    path = root / "data" / "processed" / "stocksense_decision_output.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    return df


@st.cache_data
def load_master_dataset() -> pd.DataFrame:
    root = get_project_root()
    path = root / "data" / "processed" / "master_dataset.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    return df


@st.cache_data
def load_demand_model_comparison() -> pd.DataFrame:
    root = get_project_root()
    path = root / "reports" / "demand_model_comparison.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def load_stockout_model_comparison() -> pd.DataFrame:
    root = get_project_root()
    path = root / "reports" / "stockout_model_comparison.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def load_stockout_feature_importance() -> pd.DataFrame:
    root = get_project_root()
    path = root / "reports" / "stockout_feature_importance.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def load_explainability_summary() -> pd.DataFrame:
    root = get_project_root()
    path = root / "reports" / "explainability_summary.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def format_currency(value: float) -> str:
    """Format numeric value to INR currency string."""
    return f"₹{value:,.2f}"


def get_cronza_css() -> str:
    """Return Cronza Webflow template design system CSS."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main background theme */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0b0f19 50%, #07090e 100%) !important;
        color: #f8fafc;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(13, 18, 30, 0.85) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Cronza Hero Tag */
    .cronza-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(165, 180, 252, 0.3);
        color: #a5b4fc;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 12px;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.2);
    }

    /* Gradient Title */
    .cronza-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }

    .cronza-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 24px;
    }

    /* Metric Cards - Cronza Glassmorphism */
    .metric-card {
        background: rgba(17, 24, 39, 0.65);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 20px 22px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 12px 30px -5px rgba(99, 102, 241, 0.25);
    }

    .metric-label {
        font-size: 0.8rem;
        color: #94a3b8;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: 6px;
    }

    /* Risk Badges */
    .badge-high {
        background: rgba(244, 63, 94, 0.15);
        border: 1px solid rgba(244, 63, 94, 0.4);
        color: #fecdd3;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.8rem;
    }

    .badge-medium {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.4);
        color: #fde68a;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.8rem;
    }

    .badge-low {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #a7f3d0;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.8rem;
    }

    /* Prescriptive Action Card */
    .cronza-action-card {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.8) 0%, rgba(30, 27, 75, 0.5) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-left: 6px solid #6366f1;
        border-radius: 14px;
        padding: 20px;
        margin-top: 12px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }

    /* Streamlit Tabs Customization */
    button[data-baseweb="tab"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        color: #94a3b8 !important;
        border-radius: 8px !important;
        padding: 10px 18px !important;
        margin-right: 6px !important;
        background-color: transparent !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(79, 70, 229, 0.2) 100%) !important;
        border: 1px solid rgba(165, 180, 252, 0.4) !important;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.25) !important;
    }

    /* Dataframe styling */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
    """
