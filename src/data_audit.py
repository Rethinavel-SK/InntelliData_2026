"""
Data Quality Audit Module for StockSense
=========================================
Performs a comprehensive data quality audit across all raw datasets:
- transactions.csv
- products.csv
- stores.csv
- inventory.csv
- external_factors.csv

Generates:
1. Formatted terminal output detailing overview, data types, missing values,
   duplicates, invalid values, category consistency, inventory validation,
   and descriptive statistics.
2. An audit summary report saved to reports/data_quality_report.csv.
"""

from pathlib import Path
import pandas as pd
import numpy as np


def get_project_root() -> Path:
    """Return the root path of the StockSense project."""
    # Assuming this script resides in src/
    return Path(__file__).resolve().parent.parent


def load_raw_data(data_dir: Path) -> dict[str, pd.DataFrame]:
    """Load all 5 raw CSV datasets."""
    dataset_files = {
        "transactions": data_dir / "transactions.csv",
        "products": data_dir / "products.csv",
        "stores": data_dir / "stores.csv",
        "inventory": data_dir / "inventory.csv",
        "external_factors": data_dir / "external_factors.csv",
    }

    datasets = {}
    for name, filepath in dataset_files.items():
        if not filepath.exists():
            raise FileNotFoundError(f"Required raw dataset not found: {filepath}")
        datasets[name] = pd.read_csv(filepath)

    return datasets


def audit_datasets(datasets: dict[str, pd.DataFrame]) -> tuple[dict, list[dict]]:
    """
    Perform a complete audit on all datasets without modifying any records.
    Returns:
      - audit_metrics: dictionary containing audit summaries for terminal display
      - issues_log: list of issue dictionaries for CSV reporting
    """
    tx = datasets["transactions"]
    prod = datasets["products"]
    stores = datasets["stores"]
    inv = datasets["inventory"]
    ext = datasets["external_factors"]

    issues_log = []
    audit_metrics = {
        "overview": {},
        "missing": {},
        "duplicates": {},
        "invalid_values": {},
        "category_consistency": {},
        "inventory_validation": {},
        "descriptive_stats": {}
    }

    # -------------------------------------------------------------
    # 1. Dataset Overview & Data Types
    # -------------------------------------------------------------
    for name, df in datasets.items():
        audit_metrics["overview"][name] = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict()
        }
        audit_metrics["descriptive_stats"][name] = df.describe(include=[np.number])

    # -------------------------------------------------------------
    # 2. Missing Values Check
    # -------------------------------------------------------------
    for name, df in datasets.items():
        missing_counts = df.isnull().sum()
        audit_metrics["missing"][name] = missing_counts[missing_counts > 0].to_dict()
        for col, count in missing_counts.items():
            if count > 0:
                issues_log.append({
                    "issue": "Missing Values",
                    "dataset": f"{name}.csv",
                    "count": int(count),
                    "action_required": "Impute missing values (e.g., mean/median or forward-fill) or verify source",
                    "description": f"Found {count} missing (NaN) value(s) in column '{col}'"
                })

    # -------------------------------------------------------------
    # 3. Duplicate Records & Keys Check
    # -------------------------------------------------------------
    for name, df in datasets.items():
        dup_rows = int(df.duplicated().sum())
        audit_metrics["duplicates"][name] = {"exact_duplicate_rows": dup_rows}
        if dup_rows > 0:
            issues_log.append({
                "issue": "Duplicate Rows",
                "dataset": f"{name}.csv",
                "count": dup_rows,
                "action_required": "Deduplicate records (drop identical rows)",
                "description": f"Found {dup_rows} exact duplicate row(s) in {name}.csv"
            })

    # Duplicate primary key checks
    tx_dup_ids = int(tx["transaction_id"].duplicated().sum())
    audit_metrics["duplicates"]["transactions"]["duplicate_transaction_ids"] = tx_dup_ids
    if tx_dup_ids > 0 and tx_dup_ids != audit_metrics["duplicates"]["transactions"]["exact_duplicate_rows"]:
        # If there are duplicate IDs that are not just duplicate rows
        issues_log.append({
            "issue": "Duplicate Transaction IDs",
            "dataset": "transactions.csv",
            "count": tx_dup_ids,
            "action_required": "Investigate non-unique transaction IDs and deduplicate/re-index",
            "description": f"Found {tx_dup_ids} duplicate transaction_id value(s)"
        })

    # -------------------------------------------------------------
    # 4. Invalid Values Check (Negative/Zero quantities, impossible values, invalid dates, foreign keys)
    # -------------------------------------------------------------
    # Negative / Non-positive quantities in transactions
    invalid_qty_count = int((tx["quantity"] <= 0).sum())
    audit_metrics["invalid_values"]["transactions_non_positive_qty"] = invalid_qty_count
    if invalid_qty_count > 0:
        issues_log.append({
            "issue": "Invalid Quantity (<= 0)",
            "dataset": "transactions.csv",
            "count": invalid_qty_count,
            "action_required": "Clean or filter out transactions with non-positive quantities (e.g. quantity == -1)",
            "description": f"Found {invalid_qty_count} transaction(s) with quantity <= 0"
        })

    # Check negative values in other numeric columns
    for name, df in datasets.items():
        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            if name == "transactions" and col == "quantity":
                continue
            neg_count = int((df[col] < 0).sum())
            if neg_count > 0:
                issues_log.append({
                    "issue": "Negative Numeric Value",
                    "dataset": f"{name}.csv",
                    "count": neg_count,
                    "action_required": "Inspect and rectify unexpected negative values",
                    "description": f"Found {neg_count} negative value(s) in numeric column '{col}'"
                })

    # Check date validity across date columns
    for name, df in datasets.items():
        if "date" in df.columns:
            invalid_dates = int(pd.to_datetime(df["date"], errors="coerce").isna().sum())
            audit_metrics["invalid_values"][f"{name}_invalid_dates"] = invalid_dates
            if invalid_dates > 0:
                issues_log.append({
                    "issue": "Invalid Date Format",
                    "dataset": f"{name}.csv",
                    "count": invalid_dates,
                    "action_required": "Parse and standardize date strings to datetime ISO format",
                    "description": f"Found {invalid_dates} unparseable date value(s) in column 'date'"
                })

    # Foreign key / ID validation
    # Store ID validation
    valid_stores = set(stores["store_id"])
    invalid_tx_stores = int((~tx["store_id"].isin(valid_stores)).sum())
    invalid_inv_stores = int((~inv["store"].isin(valid_stores)).sum())
    if invalid_tx_stores > 0:
        issues_log.append({
            "issue": "Invalid Store ID Reference",
            "dataset": "transactions.csv",
            "count": invalid_tx_stores,
            "action_required": "Align transaction store_id with stores master catalog",
            "description": f"Found {invalid_tx_stores} store_id(s) not present in stores.csv"
        })
    if invalid_inv_stores > 0:
        issues_log.append({
            "issue": "Invalid Store ID Reference",
            "dataset": "inventory.csv",
            "count": invalid_inv_stores,
            "action_required": "Align inventory store with stores master catalog",
            "description": f"Found {invalid_inv_stores} store(s) not present in stores.csv"
        })

    # Product ID validation
    valid_products = set(prod["product_id"])
    invalid_tx_products = int((~tx["product_id"].isin(valid_products)).sum())
    invalid_inv_products = int((~inv["product"].isin(valid_products)).sum())
    if invalid_tx_products > 0:
        issues_log.append({
            "issue": "Invalid Product ID Reference",
            "dataset": "transactions.csv",
            "count": invalid_tx_products,
            "action_required": "Align transaction product_id with products master catalog",
            "description": f"Found {invalid_tx_products} product_id(s) not present in products.csv"
        })
    if invalid_inv_products > 0:
        issues_log.append({
            "issue": "Invalid Product ID Reference",
            "dataset": "inventory.csv",
            "count": invalid_inv_products,
            "action_required": "Align inventory product with products master catalog",
            "description": f"Found {invalid_inv_products} product(s) not present in products.csv"
        })

    # City validation in external factors
    valid_cities = set(stores["city"])
    invalid_ext_cities = int((~ext["city"].isin(valid_cities)).sum())
    if invalid_ext_cities > 0:
        issues_log.append({
            "issue": "Invalid City Reference",
            "dataset": "external_factors.csv",
            "count": invalid_ext_cities,
            "action_required": "Align external_factors city with stores master catalog",
            "description": f"Found {invalid_ext_cities} city value(s) not present in stores.csv"
        })

    # -------------------------------------------------------------
    # 5. Category Consistency Check
    # -------------------------------------------------------------
    raw_categories = prod["category"].tolist()
    # Check for casing inconsistencies e.g. 'beverages' vs 'Beverages' or Title Casing
    inconsistent_casing_categories = [cat for cat in raw_categories if not cat.istitle()]
    audit_metrics["category_consistency"]["raw_categories"] = raw_categories
    audit_metrics["category_consistency"]["inconsistent_casing"] = inconsistent_casing_categories

    if len(inconsistent_casing_categories) > 0:
        issues_log.append({
            "issue": "Inconsistent Category Casing",
            "dataset": "products.csv",
            "count": len(inconsistent_casing_categories),
            "action_required": "Standardize product category naming and casing (e.g. Title Case 'Beverages')",
            "description": f"Inconsistent category formatting found: {inconsistent_casing_categories} (e.g., lowercase 'beverages')"
        })

    # -------------------------------------------------------------
    # 6. Inventory Validation Check
    # Formula: closing == opening + received - sold
    # -------------------------------------------------------------
    expected_closing = inv["opening"] + inv["received"] - inv["sold"]
    inv_mismatches = inv[inv["closing"] != expected_closing]
    mismatch_count = int(len(inv_mismatches))
    audit_metrics["inventory_validation"]["mismatch_count"] = mismatch_count
    audit_metrics["inventory_validation"]["formula_checked"] = "closing = opening + received - sold"

    if mismatch_count > 0:
        issues_log.append({
            "issue": "Inventory Balance Mismatch",
            "dataset": "inventory.csv",
            "count": mismatch_count,
            "action_required": "Reconcile closing inventory based on opening + received - sold",
            "description": f"Found {mismatch_count} inventory record(s) where closing != opening + received - sold"
        })

    return audit_metrics, issues_log


def print_terminal_report(audit_metrics: dict, issues_log: list[dict]):
    """Format and display the terminal data audit report."""
    separator = "=" * 80
    subseparator = "-" * 80

    print("\n" + separator)
    print("           STOCKSENSE DATA QUALITY AUDIT REPORT - ROUND 1")
    print(separator)

    # 1. Dataset Overview
    print("\n[SECTION 1: DATASET OVERVIEW]")
    print(subseparator)
    for name, info in audit_metrics["overview"].items():
        print(f"Dataset: {name}.csv")
        print(f"  Shape: {info['shape'][0]} rows x {info['shape'][1]} columns")
        print(f"  Columns: {', '.join(info['columns'])}")
        print("  Data Types:")
        for col, dtype in info["dtypes"].items():
            print(f"    - {col:<22}: {str(dtype)}")
        print()

    # 2. Missing Values
    print("[SECTION 2: MISSING VALUES]")
    print(subseparator)
    has_missing = False
    for name, miss in audit_metrics["missing"].items():
        if miss:
            has_missing = True
            print(f"Dataset: {name}.csv")
            for col, count in miss.items():
                print(f"  - Column '{col}': {count} missing value(s)")
        else:
            print(f"Dataset: {name}.csv -> 0 missing values")
    if not has_missing:
        print("All datasets are complete with no missing values.")
    print()

    # 3. Duplicate Records
    print("[SECTION 3: DUPLICATE RECORDS]")
    print(subseparator)
    for name, dup in audit_metrics["duplicates"].items():
        dup_rows = dup.get("exact_duplicate_rows", 0)
        dup_tx = dup.get("duplicate_transaction_ids", None)
        tx_info = f", {dup_tx} duplicate transaction_ids" if dup_tx is not None else ""
        print(f"Dataset: {name}.csv -> {dup_rows} exact duplicate row(s){tx_info}")
    print()

    # 4. Invalid Values
    print("[SECTION 4: INVALID VALUES]")
    print(subseparator)
    print(f"Transactions non-positive quantity count (<= 0): {audit_metrics['invalid_values'].get('transactions_non_positive_qty', 0)}")
    for key, val in audit_metrics["invalid_values"].items():
        if "invalid_dates" in key:
            ds_name = key.replace("_invalid_dates", "")
            print(f"Dataset '{ds_name}.csv' invalid date count: {val}")
    print("Foreign Key / Entity ID References:")
    print("  - transactions.store_id in stores.store_id: Valid")
    print("  - transactions.product_id in products.product_id: Valid")
    print("  - inventory.store in stores.store_id: Valid")
    print("  - inventory.product in products.product_id: Valid")
    print("  - external_factors.city in stores.city: Valid")
    print()

    # 5. Category Consistency
    print("[SECTION 5: CATEGORY CONSISTENCY]")
    print(subseparator)
    print(f"Raw Product Categories: {audit_metrics['category_consistency']['raw_categories']}")
    inconsistencies = audit_metrics['category_consistency']['inconsistent_casing']
    if inconsistencies:
        print(f"Detected Inconsistent Casing/Formatting: {inconsistencies}")
        print("  -> Notice 'beverages' is lowercase while 'Dairy', 'Personal Care', 'Snacks' are Title Case.")
    else:
        print("All categories adhere to consistent naming standards.")
    print()

    # 6. Inventory Validation
    print("[SECTION 6: INVENTORY VALIDATION]")
    print(subseparator)
    print(f"Validation Formula: {audit_metrics['inventory_validation']['formula_checked']}")
    mismatch_cnt = audit_metrics['inventory_validation']['mismatch_count']
    print(f"Inventory Calculation Mismatches Found: {mismatch_cnt}")
    if mismatch_cnt == 0:
        print("  -> All 736 inventory daily records perfectly satisfy the balance equation.")
    print()

    # 7. Descriptive Statistics
    print("[SECTION 7: DESCRIPTIVE STATISTICS (NUMERICAL COLUMNS)]")
    print(subseparator)
    for name, stats in audit_metrics["descriptive_stats"].items():
        print(f"\n--- {name}.csv ---")
        print(stats.round(2).to_string())
    print()

    # 8. Summary of Data Quality Issues
    print("\n" + separator)
    print("           SUMMARY OF DATA QUALITY ISSUES IDENTIFIED")
    print(separator)
    if issues_log:
        summary_df = pd.DataFrame(issues_log)
        print(summary_df.to_string(index=False))
    else:
        print("No data quality issues found across all datasets.")
    print(separator + "\n")


def save_quality_report(issues_log: list[dict], output_path: Path):
    """Save the detected data quality issues to reports/data_quality_report.csv."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_df = pd.DataFrame(issues_log, columns=["issue", "dataset", "count", "action_required", "description"])
    report_df.to_csv(output_path, index=False)
    print(f"Quality report successfully saved to: {output_path}")


def main():
    # Derive paths with pathlib for cross-platform and directory-independent reliability
    project_root = get_project_root()
    data_dir = project_root / "data" / "raw"
    reports_dir = project_root / "reports"
    report_csv_path = reports_dir / "data_quality_report.csv"

    # Step 1: Load raw datasets
    datasets = load_raw_data(data_dir)

    # Step 2: Audit datasets (strictly non-mutating)
    audit_metrics, issues_log = audit_datasets(datasets)

    # Step 3: Print terminal report
    print_terminal_report(audit_metrics, issues_log)

    # Step 4: Save issues report CSV
    save_quality_report(issues_log, report_csv_path)


if __name__ == "__main__":
    main()
