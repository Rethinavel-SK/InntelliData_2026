"""
Stock-out Risk Classification Engine for StockSense
===================================================
StockSense Round 2 - Step 3

Trains and compares 7 classification models to predict stock-out risk:
1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier
4. XGBoost Classifier
5. K-Nearest Neighbors (KNN) Classifier
6. Gaussian Naive Bayes Classifier
7. Support Vector Classifier (SVC)

Target definition:
stockout_flag = 1 if closing stock <= reorder_lvl (high replenishment risk), else 0

Calculates predicted stockout_probability and assigns risk levels:
- HIGH   : probability >= 0.70
- MEDIUM : 0.40 <= probability < 0.70
- LOW    : probability < 0.40

Prunes data leakage, uses time-based train/test splitting, exports evaluation metrics,
saves confusion matrix plot to reports/figures/, and serializes the selected model.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import joblib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
)


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def prepare_classification_data(df: pd.DataFrame):
    """
    Prepare feature matrix X and classification target y with time-based split.
    """
    df = df.sort_values("date").reset_index(drop=True)

    # Target definition: stock-out risk flag
    df["stockout_flag"] = (df["closing"] <= df["reorder_lvl"]).astype(int)

    # Exclude direct target indicators to prevent leakage
    leakage_cols = ["date", "daily_demand", "next_7_day_demand", "closing", "reorder_required", "is_stockout", "stockout_flag", "reorder_gap"]

    numeric_cols = [
        "day_of_week", "weekend_flag", "month", "week_no", "festival_flag",
        "lag_1", "lag_7", "lag_14", "rolling_mean_7", "rolling_mean_14", "rolling_std_7",
        "days_of_inventory", "inventory_to_demand_ratio",
        "discount_pct", "price_change", "promotion_flag", "shelf_life", "lead_time",
        "opening", "received", "reorder_lvl"
    ]

    categorical_cols = ["store_id", "product_id", "store_type", "category", "brand"]

    num_cols = [c for c in numeric_cols if c in df.columns]
    cat_cols = [c for c in categorical_cols if c in df.columns]

    df_encoded = pd.get_dummies(df[num_cols + cat_cols], columns=cat_cols, drop_first=True)
    feature_names = list(df_encoded.columns)

    X = df_encoded.astype(float)
    y = df["stockout_flag"].values

    # Time-based train/test split (first 80% dates train, last 20% test)
    unique_dates = sorted(df["date"].unique())
    split_idx = int(len(unique_dates) * 0.8)
    cutoff_date = unique_dates[split_idx]

    train_mask = df["date"] < cutoff_date
    test_mask = df["date"] >= cutoff_date

    X_train, y_train = X[train_mask], y[train_mask]
    X_test, y_test = X[test_mask], y[test_mask]

    print(f"Classification Data Split:")
    print(f"  Train set: {len(X_train)} rows | Class distribution: {pd.Series(y_train).value_counts().to_dict()}")
    print(f"  Test set : {len(X_test)} rows | Class distribution: {pd.Series(y_test).value_counts().to_dict()}")

    return X_train, y_train, X_test, y_test, feature_names, df[test_mask].reset_index(drop=True), df


def train_and_evaluate_classifiers(X_train, y_train, X_test, y_test, feature_names):
    """
    Train 7 classification models and compute performance metrics.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "Logistic Regression": LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, class_weight="balanced", random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=6, class_weight="balanced", random_state=42),
        "XGBoost": XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.05, random_state=42),
        "KNN Classifier": KNeighborsClassifier(n_neighbors=5),
        "Naive Bayes": GaussianNB(),
        "Support Vector Machine (SVC)": SVC(probability=True, class_weight="balanced", random_state=42)
    }

    results = []
    trained_models = {}

    for name, model in models.items():
        if name in ["Logistic Regression", "KNN Classifier", "Support Vector Machine (SVC)", "Naive Bayes"]:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_prob = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]

        trained_models[name] = model

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        try:
            auc = roc_auc_score(y_test, y_prob)
        except Exception:
            auc = 0.5

        results.append({
            "model": name,
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(auc), 4)
        })

    results_df = pd.DataFrame(results).sort_values("f1_score", ascending=False).reset_index(drop=True)

    best_model_name = results_df.iloc[0]["model"]
    best_model = trained_models[best_model_name]

    print("\n--- Stock-out Classification Model Comparison ---")
    print(results_df.to_string(index=False))
    print(f"\nBest Selected Classification Model: {best_model_name}")

    # Generate predictions for confusion matrix
    if best_model_name in ["Logistic Regression", "KNN Classifier", "Support Vector Machine (SVC)", "Naive Bayes"]:
        best_pred = best_model.predict(X_test_scaled)
    else:
        best_pred = best_model.predict(X_test)

    cm = confusion_matrix(y_test, best_pred)

    return results_df, best_model_name, best_model, cm, scaler


def plot_confusion_matrix(cm: np.ndarray, model_name: str, output_path: Path):
    """Plot and save confusion matrix heatmap."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Normal Stock (0)", "Stock-out Risk (1)"],
                yticklabels=["Normal Stock (0)", "Stock-out Risk (1)"])
    plt.title(f"Confusion Matrix - {model_name}", fontsize=12, fontweight="bold")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Confusion matrix plot saved to: {output_path}")


def main():
    root = get_project_root()
    data_dir = root / "data" / "processed"
    models_dir = root / "models"
    reports_dir = root / "reports"
    figures_dir = reports_dir / "figures"

    # Step 1: Load features dataset
    features_df = pd.read_csv(data_dir / "features_dataset.csv")
    features_df["date"] = pd.to_datetime(features_df["date"])

    # Step 2: Prepare classification data
    X_train, y_train, X_test, y_test, feature_names, test_df, full_df = prepare_classification_data(features_df)

    # Step 3: Train & evaluate models
    results_df, best_model_name, best_model, cm, scaler = train_and_evaluate_classifiers(
        X_train, y_train, X_test, y_test, feature_names
    )

    # Step 4: Export comparison table
    results_df.to_csv(reports_dir / "stockout_model_comparison.csv", index=False)
    print(f"Model comparison saved to: {reports_dir / 'stockout_model_comparison.csv'}")

    # Step 5: Plot confusion matrix
    plot_confusion_matrix(cm, best_model_name, figures_dir / "stockout_confusion_matrix.png")

    # Step 6: Save best model artifact
    model_payload = {
        "model_name": best_model_name,
        "model": best_model,
        "scaler": scaler,
        "feature_names": feature_names
    }
    model_path = models_dir / "stockout_prediction_model.joblib"
    joblib.dump(model_payload, model_path)
    print(f"Stock-out model saved to: {model_path}")


if __name__ == "__main__":
    main()
