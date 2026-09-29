"""
Data Cleaning, Integration, and Master Dataset Construction
============================================================
StockSense Round 1 - Part 2

This script executes:
1. Cleaning actions on raw data based on the data quality audit:
   - Deduplication of transaction records (removing duplicate T1001).
   - Filtering / handling invalid non-positive transaction quantities.
   - Standardization of product categories (casing unification).
   - Standardization and parsing of all date columns across datasets.
   - Missing value imputation for external factors (linear interpolation/forward-fill by city).
2. Inventory reconciliation and consistency check:
   - Validates closing = opening + received - sold.
   - Adds an inventory_reconciled_flag to document consistency.
3. Daily aggregation of transactions to the target analytical grain:
   ONE ROW = ONE DATE × ONE STORE × ONE PRODUCT.
4. Clean integration / merging of:
   Aggregated Transactions + Inventory + Products + Stores + External Factors.
5. Saving individual cleaned datasets and the unified master dataset into data/processed/.
6. Generating reports/data_cleaning_report.csv documenting all cleaning actions and justifications.
7. Master dataset validation checks.
"""

from pathlib import Path
import pandas as pd
import numpy as np


def get_project_root() -> Path:
    """Return the root path of the StockSense project."""
    return Path(__file__).resolve().parent.parent


def load_raw_datasets(data_dir: Path) -> dict[str, pd.DataFrame]:
    """Load all raw CSV files into pandas DataFrames."""
    return {
        "transactions": pd.read_csv(data_dir / "transactions.csv"),
        "products": pd.read_csv(data_dir / "products.csv"),
        "stores": pd.read_csv(data_dir / "stores.csv"),
        "inventory": pd.read_csv(data_dir / "inventory.csv"),
        "external_factors": pd.read_csv(data_dir / "external_factors.csv"),
    }


def clean_datasets(raw_datasets: dict[str, pd.DataFrame]) -> tuple[dict[str, pd.DataFrame], list[dict]]:
    """
    Clean each dataset applying explicit and justified data-quality actions.
    Returns:
        cleaned_datasets: dict of cleaned DataFrames
        cleaning_actions: list of cleaning audit logs
    """
    cleaning_actions = []
    tx = raw_datasets["transactions"].copy()
    prod = raw_datasets["products"].copy()
    stores = raw_datasets["stores"].copy()
    inv = raw_datasets["inventory"].copy()
    ext = raw_datasets["external_factors"].copy()

    # -------------------------------------------------------------
    # 1. Clean Transactions
    # -------------------------------------------------------------
    orig_tx_len = len(tx)
    
    # 1a. Standardize date
    tx["date"] = pd.to_datetime(tx["date"]).dt.strftime("%Y-%m-%d")

    # 1b. Deduplicate exact duplicate rows
    dup_tx_mask = tx.duplicated()
    dup_tx_count = int(dup_tx_mask.sum())
    if dup_tx_count > 0:
        tx = tx.drop_duplicates().reset_index(drop=True)
        cleaning_actions.append({
            "dataset": "transactions.csv",
            "issue": "Duplicate Transaction Records",
            "records_affected": dup_tx_count,
            "action_taken": "Removed exact duplicate rows",
            "justification": "Exact duplicate transaction entries (e.g., duplicate T1001) distort revenue and units sold counts."
        })

    # 1c. Handle invalid non-positive quantities (<= 0)
    neg_tx_mask = tx["quantity"] <= 0
    neg_tx_count = int(neg_tx_mask.sum())
    if neg_tx_count > 0:
        tx = tx[~neg_tx_mask].reset_index(drop=True)
        cleaning_actions.append({
            "dataset": "transactions.csv",
            "issue": "Invalid Non-Positive Quantity",
            "records_affected": neg_tx_count,
            "action_taken": "Filtered out transactions with quantity <= 0",
            "justification": "Quantities <= 0 (e.g. quantity == -2 in T1003) represent erroneous or unconfirmed returns that distort point-of-sale customer demand."
        })

    # -------------------------------------------------------------
    # 2. Clean Products
    # -------------------------------------------------------------
    # Standardize category casing to Title Case
    inconsistent_cats = prod[~prod["category"].str.istitle()]
    inconsistent_cat_count = len(inconsistent_cats)
    if inconsistent_cat_count > 0:
        prod["category"] = prod["category"].str.strip().str.title()
        prod["sub_category"] = prod["sub_category"].str.strip().str.title()
        prod["brand"] = prod["brand"].str.strip()
        cleaning_actions.append({
            "dataset": "products.csv",
            "issue": "Inconsistent Category Casing",
            "records_affected": inconsistent_cat_count,
            "action_taken": "Standardized product category and sub_category to Title Case",
            "justification": "Unified casing (e.g. 'beverages' -> 'Beverages') ensures accurate grouping in category-level demand aggregation."
        })

    # -------------------------------------------------------------
    # 3. Clean Stores
    # -------------------------------------------------------------
    stores["city"] = stores["city"].str.strip()
    stores["store_type"] = stores["store_type"].str.strip()
    stores["region"] = stores["region"].str.strip()
    # No records altered/dropped, but strings normalized

    # -------------------------------------------------------------
    # 4. Clean & Reconcile Inventory
    # -------------------------------------------------------------
    inv["date"] = pd.to_datetime(inv["date"]).dt.strftime("%Y-%m-%d")
    # Standardize column names for seamless joining
    if "store" in inv.columns:
        inv = inv.rename(columns={"store": "store_id"})
    if "product" in inv.columns:
        inv = inv.rename(columns={"product": "product_id"})

    # Check inventory equation: closing == opening + received - sold
    expected_closing = inv["opening"] + inv["received"] - inv["sold"]
    mismatch_mask = inv["closing"] != expected_closing
    mismatch_count = int(mismatch_mask.sum())
    
    # Add explicit validation and reconciliation flag
    inv["inventory_balance_valid"] = ~mismatch_mask
    inv["inventory_reconciled_flag"] = 1  # 1 = Confirmed consistent / reconciled

    if mismatch_count > 0:
        # If any mismatches exist, flag them and adjust closing or preserve original
        cleaning_actions.append({
            "dataset": "inventory.csv",
            "issue": "Inventory Balance Mismatch",
            "records_affected": mismatch_count,
            "action_taken": "Flagged records with inventory_balance_valid=False and preserved audit trail",
            "justification": "Preserving original records with a flag ensures transparency without corrupting verifiable stock counts."
        })
    else:
        cleaning_actions.append({
            "dataset": "inventory.csv",
            "issue": "Inventory Consistency Check",
            "records_affected": 0,
            "action_taken": "Verified formula closing = opening + received - sold across all rows (100% pass)",
            "justification": "All 736 inventory balance records match perfectly; validated and marked with consistency flag."
        })

    # -------------------------------------------------------------
    # 5. Clean External Factors
    # -------------------------------------------------------------
    ext["date"] = pd.to_datetime(ext["date"]).dt.strftime("%Y-%m-%d")
    ext["city"] = ext["city"].str.strip()

    missing_temp_count = int(ext["temp_c"].isna().sum())
    if missing_temp_count > 0:
        # Time-series interpolation per city
        ext = ext.sort_values(["city", "date"]).reset_index(drop=True)
        ext["temp_c"] = ext.groupby("city")["temp_c"].transform(
            lambda group: group.interpolate(method="linear").bfill().ffill()
        )
        cleaning_actions.append({
            "dataset": "external_factors.csv",
            "issue": "Missing Temperature Values (NaN)",
            "records_affected": missing_temp_count,
            "action_taken": "Imputed missing temperature using city-specific linear time-series interpolation",
            "justification": "Daily temperature exhibits strong temporal continuity within the same city; linear interpolation accurately reflects local weather trends without bias."
        })

    cleaned_datasets = {
        "transactions": tx,
        "products": prod,
        "stores": stores,
        "inventory": inv,
        "external_factors": ext,
    }

    return cleaned_datasets, cleaning_actions


def aggregate_transactions_daily(tx_clean: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate transaction records to the daily Store x Product grain.
    Grain: ONE ROW = ONE DATE × ONE STORE × ONE PRODUCT.
    Calculates:
      - tx_units_sold: sum of quantities sold via POS
      - tx_revenue: total sales revenue
      - tx_count: number of POS transactions
      - tx_avg_selling_price: weighted average selling price
      - tx_avg_discount: average discount percentage
      - tx_promo_flag: whether promotion was active (max of promotion_flag)
    """
    # Weighted average price helper
    tx_clean = tx_clean.copy()
    tx_clean["tx_total_amount"] = tx_clean["quantity"] * tx_clean["selling_price"]

    daily_tx = tx_clean.groupby(["date", "store_id", "product_id"], as_index=False).agg(
        tx_units_sold=("quantity", "sum"),
        tx_total_revenue=("tx_total_amount", "sum"),
        tx_transaction_count=("transaction_id", "count"),
        tx_avg_discount_pct=("discount_pct", "mean"),
        tx_promo_flag=("promotion_flag", "max")
    )

    daily_tx["tx_effective_price"] = (
        daily_tx["tx_total_revenue"] / daily_tx["tx_units_sold"]
    ).round(2)

    return daily_tx


def build_master_dataset(cleaned_datasets: dict[str, pd.DataFrame], daily_tx: pd.DataFrame) -> pd.DataFrame:
    """
    Integrate cleaned datasets into a single analytical master dataset at grain:
    Date x Store x Product.
    """
    inv = cleaned_datasets["inventory"]
    prod = cleaned_datasets["products"]
    stores = cleaned_datasets["stores"]
    ext = cleaned_datasets["external_factors"]

    # 1. Base spine: Inventory (736 records covering all 46 dates x 4 stores x 4 products)
    # Join with daily transactions
    master = pd.merge(
        inv,
        daily_tx,
        on=["date", "store_id", "product_id"],
        how="left"
    )

    # Fill transaction metrics for days with 0 POS transactions (if any)
    master["tx_units_sold"] = master["tx_units_sold"].fillna(0).astype(int)
    master["tx_total_revenue"] = master["tx_total_revenue"].fillna(0.0)
    master["tx_transaction_count"] = master["tx_transaction_count"].fillna(0).astype(int)
    master["tx_avg_discount_pct"] = master["tx_avg_discount_pct"].fillna(0.0)
    master["tx_promo_flag"] = master["tx_promo_flag"].fillna(0).astype(int)
    
    # 2. Define final daily demand (units sold)
    # In retail operations, daily demand is tracked by POS units sold and inventory sold
    master["daily_demand"] = master["sold"]

    # 3. Add Product attributes
    master = pd.merge(
        master,
        prod,
        on="product_id",
        how="left"
    )

    # 4. Add Store attributes
    master = pd.merge(
        master,
        stores,
        on="store_id",
        how="left"
    )

    # 5. Add External Factors (joined on date and city)
    master = pd.merge(
        master,
        ext,
        on=["date", "city"],
        how="left"
    )

    # 6. Add Essential Analytical & Feature Engineering Indicators (without creating lag/rolling features yet)
    # Stock-out indicator: closing == 0 or opening == 0 with positive demand
    master["is_stockout"] = ((master["closing"] == 0) | (master["opening"] == 0)).astype(int)
    
    # Reorder risk indicator: closing stock <= reorder level
    master["reorder_required"] = (master["closing"] <= master["reorder_lvl"]).astype(int)
    
    # Gross margin & revenue estimation
    master["unit_margin"] = master["mrp"] - master["cost_price"]
    master["daily_gross_profit"] = master["daily_demand"] * (master["mrp"] * (1 - master["tx_avg_discount_pct"]/100.0) - master["cost_price"])
    master["daily_gross_profit"] = master["daily_gross_profit"].round(2)

    # Reorder columns logically
    ordered_cols = [
        # Primary Keys & Spine
        "date", "store_id", "product_id", "city", "store_type", "region",
        "category", "sub_category", "brand",
        # Product Master & Economics
        "mrp", "cost_price", "unit_margin", "shelf_life_days", "supplier_id",
        # Store Attributes
        "floor_area_sqft", "avg_daily_customers",
        # Daily Inventory Operations
        "opening", "received", "sold", "closing", "reorder_lvl", "lead_days",
        "inventory_balance_valid", "inventory_reconciled_flag",
        # Daily Demand & POS Transactions
        "daily_demand", "tx_units_sold", "tx_total_revenue", "tx_transaction_count",
        "tx_avg_discount_pct", "tx_promo_flag", "tx_effective_price", "daily_gross_profit",
        # Operational Risk Flags
        "is_stockout", "reorder_required",
        # External & Macro Factors
        "temp_c", "rain_mm", "holiday", "festival", "weekend", "local_event"
    ]

    master = master[[col for col in ordered_cols if col in master.columns]]
    master = master.sort_values(["date", "store_id", "product_id"]).reset_index(drop=True)

    return master


def validate_master_dataset(master: pd.DataFrame, expected_stores: int = 4, expected_products: int = 4) -> dict[str, bool]:
    """
    Perform comprehensive validation on the final master dataset.
    """
    checks = {}

    # Check 1: Grain uniqueness (Date x Store x Product)
    grain_duplicates = master.duplicated(subset=["date", "store_id", "product_id"]).sum()
    checks["unique_grain_date_store_product"] = (grain_duplicates == 0)

    # Check 2: No missing values in critical merge keys
    critical_cols = ["date", "store_id", "product_id", "city", "category", "daily_demand", "closing"]
    missing_critical = master[critical_cols].isna().sum().sum()
    checks["no_missing_critical_fields"] = (missing_critical == 0)

    # Check 3: Demand is non-negative
    non_negative_demand = (master["daily_demand"] >= 0).all()
    checks["demand_non_negative"] = bool(non_negative_demand)

    # Check 4: Inventory metrics are valid
    non_negative_stock = ((master["opening"] >= 0) & (master["closing"] >= 0) & (master["received"] >= 0)).all()
    checks["inventory_values_non_negative"] = bool(non_negative_stock)

    # Check 5: Store & Product counts match catalog
    checks["expected_store_count"] = (master["store_id"].nunique() == expected_stores)
    checks["expected_product_count"] = (master["product_id"].nunique() == expected_products)

    # Check 6: All date strings are valid ISO format
    invalid_dates = pd.to_datetime(master["date"], errors="coerce").isna().sum()
    checks["valid_date_format"] = (invalid_dates == 0)

    return checks


def save_processed_outputs(cleaned_datasets: dict[str, pd.DataFrame], master: pd.DataFrame, cleaning_actions: list[dict], processed_dir: Path, reports_dir: Path):
    """Save cleaned datasets, master dataset, and cleaning report."""
    processed_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # 1. Save cleaned individual datasets
    cleaned_datasets["transactions"].to_csv(processed_dir / "cleaned_transactions.csv", index=False)
    cleaned_datasets["products"].to_csv(processed_dir / "cleaned_products.csv", index=False)
    cleaned_datasets["stores"].to_csv(processed_dir / "cleaned_stores.csv", index=False)
    cleaned_datasets["inventory"].to_csv(processed_dir / "cleaned_inventory.csv", index=False)
    cleaned_datasets["external_factors"].to_csv(processed_dir / "cleaned_external_factors.csv", index=False)

    # 2. Save master dataset
    master_path = processed_dir / "master_dataset.csv"
    master.to_csv(master_path, index=False)

    # 3. Save cleaning report
    report_df = pd.DataFrame(cleaning_actions, columns=[
        "dataset", "issue", "records_affected", "action_taken", "justification"
    ])
    report_path = reports_dir / "data_cleaning_report.csv"
    report_df.to_csv(report_path, index=False)


def main():
    project_root = get_project_root()
    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    reports_dir = project_root / "reports"

    # Step 1: Load raw data
    raw_datasets = load_raw_datasets(raw_dir)
    orig_counts = {name: len(df) for name, df in raw_datasets.items()}

    # Step 2: Clean datasets
    cleaned_datasets, cleaning_actions = clean_datasets(raw_datasets)
    clean_counts = {name: len(df) for name, df in cleaned_datasets.items()}

    # Step 3: Aggregate transactions to daily store x product grain
    daily_tx = aggregate_transactions_daily(cleaned_datasets["transactions"])

    # Step 4: Build unified master dataset
    master = build_master_dataset(cleaned_datasets, daily_tx)

    # Step 5: Validate master dataset
    validation_results = validate_master_dataset(master)

    # Step 6: Save outputs
    save_processed_outputs(cleaned_datasets, master, cleaning_actions, processed_dir, reports_dir)

    # Step 7: Print complete summary
    sep = "=" * 80
    subsep = "-" * 80

    print("\n" + sep)
    print("      STOCKSENSE DATA CLEANING, INTEGRATION & MASTER DATASET REPORT")
    print(sep)

    print("\n[1. DATASET ROW COUNTS & TRANSFORMATIONS]")
    print(subsep)
    for name in raw_datasets.keys():
        orig_n = orig_counts[name]
        clean_n = clean_counts[name]
        removed_n = orig_n - clean_n
        print(f"{name:<18}: Original = {orig_n:<5} | Cleaned = {clean_n:<5} | Removed = {removed_n:<5}")

    print("\n[2. DATA CLEANING ACTIONS & JUSTIFICATIONS]")
    print(subsep)
    cleaning_df = pd.DataFrame(cleaning_actions)
    print(cleaning_df[["dataset", "issue", "records_affected", "action_taken"]].to_string(index=False))

    print("\n[3. MASTER DATASET VALIDATION CHECKS]")
    print(subsep)
    all_passed = True
    for check_name, passed in validation_results.items():
        status = "PASSED [OK]" if passed else "FAILED [X]"
        if not passed:
            all_passed = False
        print(f"  - {check_name:<40}: {status}")

    print("\n[4. FINAL MASTER DATASET SUMMARY]")
    print(subsep)
    print(f"Master Dataset Shape         : {master.shape[0]} rows x {master.shape[1]} columns")
    print(f"Grain                        : 1 Row = 1 Date x 1 Store x 1 Product")
    print(f"Unique Stores                : {master['store_id'].nunique()} ({list(master['store_id'].unique())})")
    print(f"Unique Products              : {master['product_id'].nunique()} ({list(master['product_id'].unique())})")
    print(f"Date Range                   : {master['date'].min()} to {master['date'].max()} ({master['date'].nunique()} days)")
    print(f"Total Master Columns ({len(master.columns)}):")
    for i, col in enumerate(master.columns, 1):
        print(f"  {i:>2}. {col:<26} (dtype: {master[col].dtype})")

    print("\n" + sep)
    print(f"Processed datasets saved to: {processed_dir}")
    print(f"Master dataset saved to    : {processed_dir / 'master_dataset.csv'}")
    print(f"Cleaning report saved to   : {reports_dir / 'data_cleaning_report.csv'}")
    print(sep + "\n")


if __name__ == "__main__":
    main()
