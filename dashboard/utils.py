"""
Utility and Data Loading Helper Module for StockSense Dashboard
================================================================
StockSense Round 3 - Dashboard Utilities
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


def get_custom_css() -> str:
    """Return modern CSS styling for metric cards and badges."""
    return """
    <style>
    .metric-card {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 16px 20px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 12px;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 4px;
    }
    .badge-high {
        background-color: #ef4444;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-medium {
        background-color: #f59e0b;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-low {
        background-color: #10b981;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .action-box {
        background-color: #0f172a;
        border-left: 5px solid #ef4444;
        padding: 14px 18px;
        border-radius: 6px;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    </style>
    """
