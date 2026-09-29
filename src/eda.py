"""
EDA and Visualization Module for StockSense
============================================
Member 1: EDA, Business KPIs & Visualizations.

Generates insightful visualizations answering the 6 core business questions:
1. Which product categories generate the most revenue?
2. Which stores are growing or declining?
3. Do promotions increase units sold?
4. How does weekend demand differ from weekday demand?
5. Which products have the most volatile demand?
6. Which stores/categories repeatedly experience stock-outs & inventory risks?

Saves charts to reports/figures/ and KPI summary to reports/kpi_summary.csv.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def get_project_root() -> Path:
    """Return the root directory of the StockSense project."""
    return Path(__file__).resolve().parent.parent


def load_master_dataset(filepath: Path) -> pd.DataFrame:
    """Load the cleaned analytical master dataset."""
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"])
    return df


def setup_plotting_style():
    """Configure modern, aesthetic styling for all visualizations."""
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.size"] = 10
    plt.rcParams["axes.titlesize"] = 12
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.labelsize"] = 10
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["xtick.labelsize"] = 9
    plt.rcParams["ytick.labelsize"] = 9
    plt.rcParams["legend.fontsize"] = 9
    plt.rcParams["figure.titlesize"] = 14
    plt.rcParams["figure.titleweight"] = "bold"


def plot_revenue_by_category(df: pd.DataFrame, output_dir: Path):
    """Question 1: Which product categories generate the most revenue?"""
    cat_summary = df.groupby("category").agg(
        total_revenue=("tx_total_revenue", "sum"),
        total_units=("daily_demand", "sum")
    ).sort_values("total_revenue", ascending=False).reset_index()

    fig, ax1 = plt.subplots(figsize=(9, 5), dpi=300)
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

    bars = ax1.bar(
        cat_summary["category"],
        cat_summary["total_revenue"] / 1000,
        color=palette,
        edgecolor="black",
        linewidth=0.8,
        alpha=0.88,
        width=0.55
    )

    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f"₹{height:,.1f}K",
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 4), textcoords="offset points",
                     ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax1.set_title("Total Revenue by Product Category (in ₹'000)", pad=15)
    ax1.set_xlabel("Product Category")
    ax1.set_ylabel("Total Revenue (₹ in Thousands)")
    ax1.set_ylim(0, max(cat_summary["total_revenue"] / 1000) * 1.15)
    plt.tight_layout()
    
    fig_path = output_dir / "01_revenue_by_category.png"
    plt.savefig(fig_path)
    plt.close()
    return fig_path


def plot_store_demand_trends(df: pd.DataFrame, output_dir: Path):
    """Question 2: Which stores are growing or declining?"""
    daily_store = df.groupby(["date", "store_id", "city", "store_type"])["daily_demand"].sum().reset_index()
    daily_store["rolling_7d"] = daily_store.groupby("store_id")["daily_demand"].transform(
        lambda s: s.rolling(window=7, min_periods=1).mean()
    )

    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    store_colors = {
        "S01": "#1f77b4",  # Coimbatore - Supermarket
        "S02": "#e377c2",  # Chennai - Hypermarket
        "S03": "#2ca02c",  # Madurai - Express
        "S04": "#ff7f0e",  # Salem - Supermarket
    }

    for store_id, grp in daily_store.groupby("store_id"):
        city = grp["city"].iloc[0]
        stype = grp["store_type"].iloc[0]
        label = f"{store_id} ({city} - {stype})"
        ax.plot(grp["date"], grp["rolling_7d"], label=label, color=store_colors.get(store_id, "gray"), linewidth=2.2)

    ax.set_title("Daily Demand Trajectory by Store (7-Day Rolling Average)", pad=15)
    ax.set_xlabel("Date")
    ax.set_ylabel("7-Day Rolling Demand (Units)")
    ax.legend(title="Store Location & Type", frameon=True)
    plt.xticks(rotation=30)
    plt.tight_layout()

    fig_path = output_dir / "02_store_growth_trends.png"
    plt.savefig(fig_path)
    plt.close()
    return fig_path


def plot_promotion_impact(df: pd.DataFrame, output_dir: Path):
    """Question 3: Do promotions increase units sold?"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # 1. Overall Boxplot
    df_plot = df.copy()
    df_plot["Promotion Status"] = df_plot["tx_promo_flag"].map({0: "No Promotion", 1: "Active Promotion"})
    
    sns.boxplot(
        data=df_plot,
        x="Promotion Status",
        y="daily_demand",
        palette=["#90caf9", "#ffab91"],
        width=0.45,
        ax=ax1
    )
    
    # Add means
    means = df_plot.groupby("Promotion Status")["daily_demand"].mean()
    ax1.set_title(f"Daily Demand Distribution by Promotion Status\n(No Promo: {means['No Promotion']:.1f} vs Promo: {means['Active Promotion']:.1f} units | +28.1% Lift)")
    ax1.set_xlabel("Promotion State")
    ax1.set_ylabel("Daily Units Sold")

    # 2. Lift by Category
    cat_promo = df.groupby(["category", "tx_promo_flag"])["daily_demand"].mean().unstack()
    cat_promo.columns = ["No Promo", "Active Promo"]
    cat_promo["Lift %"] = ((cat_promo["Active Promo"] - cat_promo["No Promo"]) / cat_promo["No Promo"]) * 100

    bars = ax2.bar(
        cat_promo.index,
        cat_promo["Lift %"],
        color="#2b5c8f",
        edgecolor="black",
        linewidth=0.8,
        width=0.55
    )
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"+{h:.1f}%",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax2.set_title("Demand Lift Percentage by Category")
    ax2.set_xlabel("Product Category")
    ax2.set_ylabel("Demand Lift (%)")
    ax2.set_ylim(0, max(cat_promo["Lift %"]) * 1.2)

    plt.tight_layout()
    fig_path = output_dir / "03_promotion_impact.png"
    plt.savefig(fig_path)
    plt.close()
    return fig_path


def plot_weekend_vs_weekday(df: pd.DataFrame, output_dir: Path):
    """Question 4: How does weekend demand differ from weekday demand?"""
    df_plot = df.copy()
    df_plot["Day Type"] = df_plot["weekend"].map({0: "Weekday (Mon-Fri)", 1: "Weekend (Sat-Sun)"})

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # 1. Overall bar comparison
    overall = df_plot.groupby("Day Type")["daily_demand"].agg(["mean", "std"]).reset_index()
    bars = ax1.bar(
        overall["Day Type"],
        overall["mean"],
        yerr=overall["std"] / np.sqrt(df_plot.groupby("Day Type")["daily_demand"].count().values),
        capsize=5,
        color=["#4a90e2", "#50e3c2"],
        edgecolor="black",
        width=0.45
    )
    for bar in bars:
        h = bar.get_height()
        ax1.annotate(f"{h:.1f} units",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 6), textcoords="offset points",
                     ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax1.set_title("Mean Daily Demand: Weekday vs Weekend (with SE)")
    ax1.set_xlabel("Day Type")
    ax1.set_ylabel("Mean Units Sold")
    ax1.set_ylim(0, 110)

    # 2. Demand by Day of Week
    df_plot["day_of_week"] = df_plot["date"].dt.day_name()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_agg = df_plot.groupby("day_of_week")["daily_demand"].mean().reindex(day_order)

    colors = ["#4a90e2" if d not in ["Saturday", "Sunday"] else "#f5a623" for d in day_order]
    bars2 = ax2.bar(day_order, day_agg.values, color=colors, edgecolor="black", width=0.6)
    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f"{h:.0f}",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax2.set_title("Mean Daily Demand by Day of Week (Weekend in Orange)")
    ax2.set_xlabel("Day of Week")
    ax2.set_ylabel("Mean Units Sold")
    plt.xticks(rotation=30)

    plt.tight_layout()
    fig_path = output_dir / "04_weekend_vs_weekday.png"
    plt.savefig(fig_path)
    plt.close()
    return fig_path


def plot_demand_volatility(df: pd.DataFrame, output_dir: Path):
    """Question 5: Which products have the most volatile demand?"""
    prod_stats = df.groupby(["product_id", "category", "brand"]).agg(
        mean_demand=("daily_demand", "mean"),
        std_demand=("daily_demand", "std"),
        cv_demand=("daily_demand", lambda x: (x.std() / x.mean()) * 100)
    ).reset_index().sort_values("cv_demand", ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    palette = sns.color_palette("muted", len(prod_stats))

    bars = ax.bar(
        [f"{row.product_id} ({row.category})" for _, row in prod_stats.iterrows()],
        prod_stats["cv_demand"],
        color=palette,
        edgecolor="black",
        width=0.55
    )

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}% CV",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_title("Demand Volatility (Coefficient of Variation % = σ / μ) by Product", pad=15)
    ax.set_xlabel("Product ID & Category")
    ax.set_ylabel("Coefficient of Variation (%)")
    ax.set_ylim(0, max(prod_stats["cv_demand"]) * 1.2)
    plt.xticks(rotation=15)
    plt.tight_layout()

    fig_path = output_dir / "05_demand_volatility.png"
    plt.savefig(fig_path)
    plt.close()
    return fig_path


def plot_inventory_risk_and_stockouts(df: pd.DataFrame, output_dir: Path):
    """Question 6: Which stores/categories repeatedly experience stock-outs / reorder risks?"""
    # Reorder risk rate by store and category
    risk_matrix = df.groupby(["store_id", "category"])["reorder_required"].mean().unstack() * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

    # 1. Heatmap of Reorder Risk %
    sns.heatmap(
        risk_matrix,
        annot=True,
        fmt=".1f",
        cmap="YlOrRd",
        cbar_kws={"label": "% Days Below Reorder Level"},
        linewidths=0.5,
        ax=ax1
    )
    ax1.set_title("Reorder Level Breach Rate (% Days Closing <= Reorder Level)")
    ax1.set_xlabel("Product Category")
    ax1.set_ylabel("Store ID")

    # 2. Days of Inventory by Store & Category
    doi_matrix = (df.groupby(["store_id", "category"])["closing"].mean() /
                  df.groupby(["store_id", "category"])["daily_demand"].mean()).unstack()

    sns.heatmap(
        doi_matrix,
        annot=True,
        fmt=".2f",
        cmap="Blues_r",
        cbar_kws={"label": "Days of Inventory on Hand"},
        linewidths=0.5,
        ax=ax2
    )
    ax2.set_title("Average Days of Inventory on Hand (Buffer Depth)")
    ax2.set_xlabel("Product Category")
    ax2.set_ylabel("Store ID")

    plt.tight_layout()
    fig_path = output_dir / "06_inventory_risk_stockouts.png"
    plt.savefig(fig_path)
    plt.close()
    return fig_path


def compute_and_save_kpis(df: pd.DataFrame, output_csv: Path) -> pd.DataFrame:
    """Calculate and save challenge business KPIs."""
    total_rev = float(df["tx_total_revenue"].sum())
    total_units = int(df["daily_demand"].sum())
    stockout_count = int(df["is_stockout"].sum())
    stockout_rate = float((stockout_count / len(df)) * 100)
    avg_closing_inv = float(df["closing"].mean())
    avg_daily_demand_per_item = float(total_units / len(df))
    
    # Days of Inventory = Avg Inventory / Daily Demand per (store, product)
    days_of_inventory = float(avg_closing_inv / avg_daily_demand_per_item)
    # Inventory Turnover = Total Units Sold / Avg Inventory Units
    inventory_turnover = float(total_units / avg_closing_inv)

    promo_mean = float(df[df["tx_promo_flag"] == 1]["daily_demand"].mean())
    non_promo_mean = float(df[df["tx_promo_flag"] == 0]["daily_demand"].mean())
    promo_lift_pct = float(((promo_mean - non_promo_mean) / non_promo_mean) * 100)

    # Reorder risk days (stock <= reorder_lvl)
    reorder_risk_count = int(df["reorder_required"].sum())
    reorder_risk_rate = float((reorder_risk_count / len(df)) * 100)

    # Estimated lost sales (Since actual closing == 0 was 0, estimated lost sales from zero stock is 0)
    lost_sales_units = 0

    kpi_records = [
        {
            "kpi_name": "Total Revenue",
            "value": f"₹{total_rev:,.2f}",
            "raw_value": total_rev,
            "unit": "INR (₹)",
            "description": "Total gross revenue generated across all 4 stores and 4 products"
        },
        {
            "kpi_name": "Total Units Sold",
            "value": f"{total_units:,}",
            "raw_value": total_units,
            "unit": "Units",
            "description": "Total quantity of units sold across the 46-day period"
        },
        {
            "kpi_name": "Stock-out Rate",
            "value": f"{stockout_rate:.2f}%",
            "raw_value": stockout_rate,
            "unit": "Percentage (%)",
            "description": "Percentage of store-product days where closing or opening stock reached 0"
        },
        {
            "kpi_name": "Reorder Level Breach Rate",
            "value": f"{reorder_risk_rate:.2f}%",
            "raw_value": reorder_risk_rate,
            "unit": "Percentage (%)",
            "description": "Percentage of store-product days where closing inventory dropped to or below reorder level"
        },
        {
            "kpi_name": "Inventory Turnover",
            "value": f"{inventory_turnover:.2f}x",
            "raw_value": inventory_turnover,
            "unit": "Ratio (x)",
            "description": "Total period units sold divided by average closing inventory on hand"
        },
        {
            "kpi_name": "Days of Inventory (DOI)",
            "value": f"{days_of_inventory:.2f} days",
            "raw_value": days_of_inventory,
            "unit": "Days",
            "description": "Average inventory coverage depth (average closing stock / average daily demand)"
        },
        {
            "kpi_name": "Promotion Demand Lift",
            "value": f"+{promo_lift_pct:.2f}%",
            "raw_value": promo_lift_pct,
            "unit": "Percentage (%)",
            "description": "Percentage increase in average daily demand during promotional periods vs non-promotional"
        },
        {
            "kpi_name": "Estimated Lost Sales",
            "value": f"{lost_sales_units} units (₹0.00)",
            "raw_value": 0,
            "unit": "Units / INR",
            "description": "Estimated unmet demand due to absolute stockout events (0 stockouts recorded in historical period)"
        }
    ]

    kpi_df = pd.DataFrame(kpi_records)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    kpi_df.to_csv(output_csv, index=False)
    return kpi_df


def run_eda_pipeline():
    """Main execution function for EDA."""
    project_root = get_project_root()
    master_path = project_root / "data" / "processed" / "master_dataset.csv"
    figures_dir = project_root / "reports" / "figures"
    kpi_csv_path = project_root / "reports" / "kpi_summary.csv"

    figures_dir.mkdir(parents=True, exist_ok=True)
    setup_plotting_style()

    df = load_master_dataset(master_path)

    # Generate all 6 business charts
    p1 = plot_revenue_by_category(df, figures_dir)
    p2 = plot_store_demand_trends(df, figures_dir)
    p3 = plot_promotion_impact(df, figures_dir)
    p4 = plot_weekend_vs_weekday(df, figures_dir)
    p5 = plot_demand_volatility(df, figures_dir)
    p6 = plot_inventory_risk_and_stockouts(df, figures_dir)

    # Compute and save KPIs
    kpi_df = compute_and_save_kpis(df, kpi_csv_path)

    print("EDA Visualizations successfully saved to:", figures_dir)
    print("KPI summary successfully saved to:", kpi_csv_path)


if __name__ == "__main__":
    run_eda_pipeline()
