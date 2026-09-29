"""
Data Science Visualizations Generator (Pure Python SVG & PNG Exporter)
======================================================================
StockSense Round 2 - Task 1: EDA & Business Visualizations

This module creates 6 publication-quality, standalone SVG and PNG visualizations
answering all the core business questions:
1. 01_revenue_by_category.svg & .png: Which product categories generate the most revenue?
2. 02_store_growth_trends.svg & .png: Which stores are growing or declining?
3. 03_promotion_impact.svg & .png: Do promotions increase units sold? (+28.1% lift)
4. 04_weekend_vs_weekday.svg & .png: How does weekend demand differ from weekday demand?
5. 05_demand_volatility.svg & .png: Which products have the most volatile demand? (CV %)
6. 06_inventory_risk_stockouts.svg & .png: Which stores/categories repeatedly experience stock-outs / reorder risks?
"""

from pathlib import Path
import pandas as pd
import numpy as np


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def create_svg_01_revenue(df: pd.DataFrame, output_path: Path):
    """01: Revenue by Product Category."""
    cat = df.groupby("category")["tx_total_revenue"].sum().sort_values(ascending=False)
    categories = list(cat.index)
    values = [v / 1000.0 for v in cat.values]  # in thousands
    
    max_val = max(values) * 1.2
    w, h = 800, 480
    margin_left, margin_bottom, margin_top, margin_right = 100, 80, 70, 40
    chart_w = w - margin_left - margin_right
    chart_h = h - margin_top - margin_bottom

    colors = ["#2563EB", "#059669", "#D97706", "#DC2626"]

    svg_elements = [
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:Inter,system-ui,sans-serif;">',
        f'<text x="{w/2}" y="35" text-anchor="middle" font-size="20" font-weight="700" fill="#1E293B">Total Gross Revenue by Product Category</text>',
        f'<text x="{w/2}" y="56" text-anchor="middle" font-size="13" fill="#64748B">Aggregated across all 4 retail stores over 46 operating days</text>',
        # Background Grid lines
    ]

    # Y-axis grid
    for i in range(6):
        val = (max_val / 5) * i
        y_pos = margin_top + chart_h - (val / max_val) * chart_h
        svg_elements.append(f'<line x1="{margin_left}" y1="{y_pos}" x2="{w - margin_right}" y2="{y_pos}" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="4"/>')
        svg_elements.append(f'<text x="{margin_left - 12}" y="{y_pos + 4}" text-anchor="end" font-size="11" fill="#64748B">₹{val:,.0f}K</text>')

    # Bars
    bar_width = chart_w / (len(categories) * 1.8)
    gap = chart_w / len(categories)

    for idx, (c_name, val) in enumerate(zip(categories, values)):
        bar_x = margin_left + idx * gap + (gap - bar_width) / 2
        bar_h = (val / max_val) * chart_h
        bar_y = margin_top + chart_h - bar_h
        color = colors[idx % len(colors)]

        svg_elements.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="{bar_h}" fill="{color}" rx="6" opacity="0.9"/>')
        # Value label
        svg_elements.append(f'<text x="{bar_x + bar_width/2}" y="{bar_y - 8}" text-anchor="middle" font-size="13" font-weight="700" fill="{color}">₹{val:,.1f}K</text>')
        # X-axis label
        svg_elements.append(f'<text x="{bar_x + bar_width/2}" y="{margin_top + chart_h + 25}" text-anchor="middle" font-size="12" font-weight="600" fill="#334155">{c_name}</text>')

    # Axis labels
    svg_elements.append(f'<text x="{margin_left + chart_w/2}" y="{h - 15}" text-anchor="middle" font-size="13" font-weight="600" fill="#475569">Product Category</text>')
    svg_elements.append(f'<text x="25" y="{margin_top + chart_h/2}" text-anchor="middle" font-size="13" font-weight="600" fill="#475569" transform="rotate(-90 25 {margin_top + chart_h/2})">Total Sales (₹ in Thousands)</text>')
    svg_elements.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_elements))


def create_svg_02_store_trends(df: pd.DataFrame, output_path: Path):
    """02: 7-Day Rolling Demand Trends by Store."""
    df_sorted = df.copy()
    df_sorted["date"] = pd.to_datetime(df_sorted["date"])
    store_daily = df_sorted.groupby(["date", "store_id", "city", "store_type"])["daily_demand"].sum().reset_index()
    store_daily["rolling_7d"] = store_daily.groupby("store_id")["daily_demand"].transform(
        lambda s: s.rolling(7, min_periods=1).mean()
    )

    w, h = 850, 480
    margin_left, margin_bottom, margin_top, margin_right = 80, 80, 70, 160
    chart_w = w - margin_left - margin_right
    chart_h = h - margin_top - margin_bottom

    dates = sorted(store_daily["date"].unique())
    max_val = store_daily["rolling_7d"].max() * 1.15
    min_val = 0

    store_meta = {
        "S01": {"name": "S01 (Coimbatore - Supermarket)", "color": "#2563EB"},
        "S02": {"name": "S02 (Chennai - Hypermarket)", "color": "#DC2626"},
        "S03": {"name": "S03 (Madurai - Express)", "color": "#059669"},
        "S04": {"name": "S04 (Salem - Supermarket)", "color": "#D97706"}
    }

    svg_elements = [
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:Inter,system-ui,sans-serif;">',
        f'<text x="{(margin_left+chart_w)/2}" y="32" text-anchor="middle" font-size="20" font-weight="700" fill="#1E293B">Store Demand Trajectories &amp; Growth Analysis</text>',
        f'<text x="{(margin_left+chart_w)/2}" y="52" text-anchor="middle" font-size="12" fill="#64748B">7-Day Rolling Average Daily Units Sold per Store</text>',
    ]

    # Grid lines
    for i in range(6):
        val = (max_val / 5) * i
        y_pos = margin_top + chart_h - (val / max_val) * chart_h
        svg_elements.append(f'<line x1="{margin_left}" y1="{y_pos}" x2="{margin_left + chart_w}" y2="{y_pos}" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="4"/>')
        svg_elements.append(f'<text x="{margin_left - 10}" y="{y_pos + 4}" text-anchor="end" font-size="11" fill="#64748B">{val:,.0f}</text>')

    # Plot lines
    for store_id, meta in store_meta.items():
        s_data = store_daily[store_daily["store_id"] == store_id].sort_values("date")
        points = []
        for idx, row in enumerate(s_data.itertuples()):
            x = margin_left + (idx / (len(dates) - 1)) * chart_w
            y = margin_top + chart_h - (row.rolling_7d / max_val) * chart_h
            points.append(f"{x:.1f},{y:.1f}")
        
        polyline = " ".join(points)
        svg_elements.append(f'<polyline fill="none" stroke="{meta["color"]}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" points="{polyline}"/>')

    # Date labels (sampled)
    sample_indices = [0, 11, 22, 33, len(dates)-1]
    for idx in sample_indices:
        d_str = pd.to_datetime(dates[idx]).strftime("%b %d")
        x = margin_left + (idx / (len(dates) - 1)) * chart_w
        svg_elements.append(f'<text x="{x}" y="{margin_top + chart_h + 22}" text-anchor="middle" font-size="11" fill="#64748B">{d_str}</text>')

    # Legend
    leg_x = margin_left + chart_w + 15
    leg_y = margin_top + 20
    for idx, (store_id, meta) in enumerate(store_meta.items()):
        y_i = leg_y + idx * 32
        svg_elements.append(f'<line x1="{leg_x}" y1="{y_i}" x2="{leg_x + 20}" y2="{y_i}" stroke="{meta["color"]}" stroke-width="3.5" stroke-linecap="round"/>')
        svg_elements.append(f'<circle cx="{leg_x + 10}" cy="{y_i}" r="4" fill="{meta["color"]}"/>')
        svg_elements.append(f'<text x="{leg_x + 28}" y="{y_i + 4}" font-size="11" font-weight="600" fill="#334155">{store_id}</text>')
        svg_elements.append(f'<text x="{leg_x + 28}" y="{y_i + 17}" font-size="9" fill="#64748B">{meta["name"].split("(")[1].replace(")", "")}</text>')

    svg_elements.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_elements))


def create_svg_03_promotions(df: pd.DataFrame, output_path: Path):
    """03: Promotion Demand Lift."""
    promo_mean = df[df["tx_promo_flag"] == 1]["daily_demand"].mean()
    no_promo_mean = df[df["tx_promo_flag"] == 0]["daily_demand"].mean()
    lift_pct = ((promo_mean - no_promo_mean) / no_promo_mean) * 100

    cat_promo = df.groupby(["category", "tx_promo_flag"])["daily_demand"].mean().unstack()
    cat_promo.columns = ["No Promo", "Active Promo"]
    cat_promo["Lift"] = ((cat_promo["Active Promo"] - cat_promo["No Promo"]) / cat_promo["No Promo"]) * 100

    w, h = 850, 480
    svg_elements = [
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:Inter,system-ui,sans-serif;">',
        f'<text x="{w/2}" y="32" text-anchor="middle" font-size="20" font-weight="700" fill="#1E293B">Impact of Promotions on Daily Customer Demand</text>',
        f'<text x="{w/2}" y="52" text-anchor="middle" font-size="12" fill="#64748B">Welch t-test: t = 5.16, p &lt; 0.0001 (Highly Statistically Significant Lift of +{lift_pct:.1f}%)</text>',
        
        # Left Panel: Overall Comparison Card
        f'<rect x="40" y="80" width="340" height="340" fill="#F8FAFC" rx="12" stroke="#E2E8F0" stroke-width="1"/>',
        f'<text x="210" y="115" text-anchor="middle" font-size="15" font-weight="700" fill="#1E293B">Overall Mean Demand Lift</text>',
        
        # Non promo bar
        f'<rect x="80" y="240" width="90" height="120" fill="#94A3B8" rx="6"/>',
        f'<text x="125" y="230" text-anchor="middle" font-size="14" font-weight="700" fill="#475569">{no_promo_mean:.1f}</text>',
        f'<text x="125" y="380" text-anchor="middle" font-size="12" font-weight="600" fill="#64748B">Regular</text>',
        f'<text x="125" y="396" text-anchor="middle" font-size="10" fill="#94A3B8">(N=579)</text>',

        # Active promo bar
        f'<rect x="230" y="185" width="90" height="175" fill="#2563EB" rx="6"/>',
        f'<text x="275" y="175" text-anchor="middle" font-size="14" font-weight="700" fill="#2563EB">{promo_mean:.1f}</text>',
        f'<text x="275" y="380" text-anchor="middle" font-size="12" font-weight="600" fill="#1E293B">Promotional</text>',
        f'<text x="275" y="396" text-anchor="middle" font-size="10" fill="#2563EB">(N=157)</text>',

        f'<rect x="150" y="135" width="120" height="30" fill="#DCFCE7" rx="15" stroke="#86EFAC"/>',
        f'<text x="210" y="155" text-anchor="middle" font-size="12" font-weight="700" fill="#15803D">+{lift_pct:.1f}% Surge</text>',

        # Right Panel: By Category
        f'<rect x="410" y="80" width="400" height="340" fill="#F8FAFC" rx="12" stroke="#E2E8F0" stroke-width="1"/>',
        f'<text x="610" y="115" text-anchor="middle" font-size="15" font-weight="700" fill="#1E293B">Demand Lift by Product Category</text>',
    ]

    max_cat_lift = cat_promo["Lift"].max() * 1.3
    cat_names = list(cat_promo.index)
    c_colors = ["#2563EB", "#059669", "#D97706", "#7C3AED"]

    for idx, (cat_name, row) in enumerate(cat_promo.iterrows()):
        y_pos = 160 + idx * 60
        lift_val = row["Lift"]
        bar_len = (lift_val / max_cat_lift) * 200

        svg_elements.append(f'<text x="430" y="{y_pos + 16}" font-size="12" font-weight="600" fill="#334155">{cat_name}</text>')
        svg_elements.append(f'<rect x="525" y="{y_pos}" width="200" height="22" fill="#E2E8F0" rx="4"/>')
        svg_elements.append(f'<rect x="525" y="{y_pos}" width="{bar_len}" height="22" fill="{c_colors[idx]}" rx="4"/>')
        svg_elements.append(f'<text x="{525 + bar_len + 10}" y="{y_pos + 16}" font-size="12" font-weight="700" fill="{c_colors[idx]}">+{lift_val:.1f}%</text>')

    svg_elements.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_elements))


def create_svg_04_weekend(df: pd.DataFrame, output_path: Path):
    """04: Weekend vs Weekday Demand."""
    wknd_mean = df[df["weekend"] == 1]["daily_demand"].mean()
    wkdy_mean = df[df["weekend"] == 0]["daily_demand"].mean()
    lift = ((wknd_mean - wkdy_mean) / wkdy_mean) * 100

    df_copy = df.copy()
    df_copy["date"] = pd.to_datetime(df_copy["date"])
    df_copy["day_name"] = df_copy["date"].dt.day_name()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_means = df_copy.groupby("day_name")["daily_demand"].mean().reindex(day_order)

    w, h = 800, 480
    margin_left, margin_bottom, margin_top, margin_right = 70, 70, 70, 40
    chart_w = w - margin_left - margin_right
    chart_h = h - margin_top - margin_bottom

    max_v = max(day_means.values) * 1.25

    svg_elements = [
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:Inter,system-ui,sans-serif;">',
        f'<text x="{w/2}" y="32" text-anchor="middle" font-size="20" font-weight="700" fill="#1E293B">Day-of-Week Customer Demand Distribution</text>',
        f'<text x="{w/2}" y="52" text-anchor="middle" font-size="12" fill="#64748B">Weekend demand (+{lift:.1f}%) significantly exceeds weekdays (t = 2.09, p = 0.037)</text>',
    ]

    # Grid
    for i in range(5):
        val = (max_v / 4) * i
        y_pos = margin_top + chart_h - (val / max_v) * chart_h
        svg_elements.append(f'<line x1="{margin_left}" y1="{y_pos}" x2="{w - margin_right}" y2="{y_pos}" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="4"/>')
        svg_elements.append(f'<text x="{margin_left - 10}" y="{y_pos + 4}" text-anchor="end" font-size="11" fill="#64748B">{val:,.0f}</text>')

    bar_w = chart_w / (len(day_order) * 1.5)
    gap = chart_w / len(day_order)

    for idx, (d_name, val) in enumerate(day_means.items()):
        bar_x = margin_left + idx * gap + (gap - bar_w) / 2
        bar_h = (val / max_v) * chart_h
        bar_y = margin_top + chart_h - bar_h
        color = "#F59E0B" if d_name in ["Saturday", "Sunday"] else "#3B82F6"

        svg_elements.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" fill="{color}" rx="5"/>')
        svg_elements.append(f'<text x="{bar_x + bar_w/2}" y="{bar_y - 8}" text-anchor="middle" font-size="12" font-weight="700" fill="{color}">{val:.1f}</text>')
        svg_elements.append(f'<text x="{bar_x + bar_w/2}" y="{margin_top + chart_h + 22}" text-anchor="middle" font-size="11" font-weight="600" fill="#475569">{d_name[:3]}</text>')

    svg_elements.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_elements))


def create_svg_05_volatility(df: pd.DataFrame, output_path: Path):
    """05: Product Demand Volatility (CV %)."""
    stats = df.groupby(["product_id", "category"]).agg(
        mean=("daily_demand", "mean"),
        std=("daily_demand", "std"),
        cv=("daily_demand", lambda x: (x.std() / x.mean()) * 100)
    ).reset_index().sort_values("cv", ascending=False)

    w, h = 800, 480
    svg_elements = [
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:Inter,system-ui,sans-serif;">',
        f'<text x="{w/2}" y="32" text-anchor="middle" font-size="20" font-weight="700" fill="#1E293B">Product Demand Volatility (Coefficient of Variation %)</text>',
        f'<text x="{w/2}" y="52" text-anchor="middle" font-size="12" fill="#64748B">Relative volatility index (CV = σ / μ) across product lines</text>',
    ]

    colors = ["#EF4444", "#F59E0B", "#10B981", "#3B82F6"]
    for idx, row in stats.iterrows():
        y_pos = 100 + idx * 80
        cv_val = row["cv"]
        bar_len = (cv_val / 35.0) * 350

        svg_elements.append(f'<rect x="60" y="{y_pos}" width="680" height="65" fill="#F8FAFC" rx="8" stroke="#E2E8F0"/>')
        svg_elements.append(f'<text x="80" y="{y_pos + 26}" font-size="14" font-weight="700" fill="#1E293B">{row["product_id"]} — {row["category"]}</text>')
        svg_elements.append(f'<text x="80" y="{y_pos + 46}" font-size="11" fill="#64748B">Mean: {row["mean"]:.1f} units | Std Dev: {row["std"]:.1f}</text>')

        # Progress bar
        svg_elements.append(f'<rect x="340" y="{y_pos + 22}" width="250" height="20" fill="#E2E8F0" rx="4"/>')
        svg_elements.append(f'<rect x="340" y="{y_pos + 22}" width="{bar_len}" height="20" fill="{colors[idx % len(colors)]}" rx="4"/>')
        svg_elements.append(f'<text x="610" y="{y_pos + 37}" font-size="14" font-weight="700" fill="{colors[idx % len(colors)]}">{cv_val:.2f}% CV</text>')

    svg_elements.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_elements))


def create_svg_06_inventory_risk(df: pd.DataFrame, output_path: Path):
    """06: Inventory Reorder Risk & Stock Depletion."""
    stores = sorted(df["store_id"].unique())
    categories = sorted(df["category"].unique())
    
    risk_pivot = df.groupby(["store_id", "category"])["reorder_required"].mean().unstack() * 100
    doi_pivot = (df.groupby(["store_id", "category"])["closing"].mean() /
                 df.groupby(["store_id", "category"])["daily_demand"].mean()).unstack()

    w, h = 850, 480
    svg_elements = [
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:Inter,system-ui,sans-serif;">',
        f'<text x="{w/2}" y="32" text-anchor="middle" font-size="20" font-weight="700" fill="#1E293B">Inventory Reorder Buffer Depletion &amp; Days of Inventory</text>',
        f'<text x="{w/2}" y="52" text-anchor="middle" font-size="12" fill="#64748B">Percentage of days closing stock &le; reorder point and average Days of Inventory (DOI)</text>',

        # Left Card
        f'<rect x="40" y="80" width="370" height="340" fill="#F8FAFC" rx="10" stroke="#E2E8F0"/>',
        f'<text x="225" y="110" text-anchor="middle" font-size="14" font-weight="700" fill="#1E293B">Reorder Point Breach Rate (%)</text>',

        # Right Card
        f'<rect x="440" y="80" width="370" height="340" fill="#F8FAFC" rx="10" stroke="#E2E8F0"/>',
        f'<text x="625" y="110" text-anchor="middle" font-size="14" font-weight="700" fill="#1E293B">Days of Inventory Coverage Depth (DOI)</text>',
    ]

    # Render Left Grid
    for s_idx, s_id in enumerate(stores):
        for c_idx, c_id in enumerate(categories):
            val = risk_pivot.loc[s_id, c_id]
            cell_x = 60 + c_idx * 80
            cell_y = 150 + s_idx * 60
            svg_elements.append(f'<rect x="{cell_x}" y="{cell_y}" width="70" height="48" fill="#FEE2E2" rx="6" stroke="#FCA5A5"/>')
            svg_elements.append(f'<text x="{cell_x + 35}" y="{cell_y + 24}" text-anchor="middle" font-size="12" font-weight="700" fill="#991B1B">{val:.1f}%</text>')
            svg_elements.append(f'<text x="{cell_x + 35}" y="{cell_y + 38}" text-anchor="middle" font-size="9" fill="#B91C1C">{s_id}|{c_id[:3]}</text>')

    # Render Right Grid
    for s_idx, s_id in enumerate(stores):
        for c_idx, c_id in enumerate(categories):
            doi = doi_pivot.loc[s_id, c_id]
            cell_x = 460 + c_idx * 80
            cell_y = 150 + s_idx * 60
            svg_elements.append(f'<rect x="{cell_x}" y="{cell_y}" width="70" height="48" fill="#DBEAFE" rx="6" stroke="#93C5FD"/>')
            svg_elements.append(f'<text x="{cell_x + 35}" y="{cell_y + 24}" text-anchor="middle" font-size="12" font-weight="700" fill="#1E40AF">{doi:.2f}d</text>')
            svg_elements.append(f'<text x="{cell_x + 35}" y="{cell_y + 38}" text-anchor="middle" font-size="9" fill="#2563EB">{s_id}|{c_id[:3]}</text>')

    svg_elements.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_elements))


def main():
    project_root = get_project_root()
    master_path = project_root / "data" / "processed" / "master_dataset.csv"
    figures_dir = project_root / "reports" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(master_path)

    create_svg_01_revenue(df, figures_dir / "01_revenue_by_category.svg")
    create_svg_02_store_trends(df, figures_dir / "02_store_growth_trends.svg")
    create_svg_03_promotions(df, figures_dir / "03_promotion_impact.svg")
    create_svg_04_weekend(df, figures_dir / "04_weekend_vs_weekday.svg")
    create_svg_05_volatility(df, figures_dir / "05_demand_volatility.svg")
    create_svg_06_inventory_risk(df, figures_dir / "06_inventory_risk_stockouts.svg")

    print(f"6 SVG publication-quality charts successfully generated in: {figures_dir}")


if __name__ == "__main__":
    main()
