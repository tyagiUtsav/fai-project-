"""
Reproducible training script for Verdikt's churn-risk model.

Reuses the exact pipeline already validated in the research phase:
StandardScaler + OneHotEncoder -> RandomForestClassifier(300 trees,
class_weight="balanced"), 80/20 stratified split, random_state=42.

Run directly to (re)produce models/model.joblib and models/metrics.json:

    python train_model.py
"""
import json
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "data", "Customer_Transactions.csv")
MODEL_PATH = os.path.join(HERE, "models", "model.joblib")
METRICS_PATH = os.path.join(HERE, "models", "metrics.json")

NUM_COLS = [
    "age", "annual_income", "spending_score", "num_purchases", "avg_purchase_value",
    "membership_years", "website_visits_per_month", "cart_abandon_rate",
]
CAT_COLS = ["gender", "country"]
TARGET = "churned"


def train():
    df = pd.read_csv(DATA_PATH)
    X = df[NUM_COLS + CAT_COLS]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pre = ColumnTransformer([
        ("num", StandardScaler(), NUM_COLS),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS),
    ])
    clf = RandomForestClassifier(
        n_estimators=300, max_depth=8, class_weight="balanced", random_state=42
    )
    pipe = Pipeline([("pre", pre), ("clf", clf)])
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]

    metrics = {
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
        "n_test": len(y_test),
        "model_name": "RandomForestClassifier(n_estimators=300, class_weight='balanced')",
        "overall_churn_rate": round(float(df[TARGET].mean()), 4),
        "n_records": len(df),
    }

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"pipeline": pipe, "num_cols": NUM_COLS, "cat_cols": CAT_COLS}, MODEL_PATH)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print("Trained and saved model to", MODEL_PATH)
    print(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    train()
