"""
ML service: loads the trained churn-risk artifact once at startup and
exposes scoring over arbitrary customer segments of the seed dataset.

This module never retrains on request — training is a separate, explicit,
reproducible step (see train_model.py). It only scores.
"""
import os
import json
import joblib
import pandas as pd
from functools import lru_cache
from dataclasses import dataclass
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(HERE, "..", "models", "model.joblib")
METRICS_PATH = os.path.join(HERE, "..", "models", "metrics.json")
DATA_PATH = os.path.join(HERE, "..", "data", "Customer_Transactions.csv")

DISCLAIMER = (
    "Risk score — not a guarantee. This model ranks churn risk; it does not "
    "prove that any intervention caused a customer to stay. See model metrics "
    "for this model's real, measured precision/recall on held-out data."
)


@dataclass
class SegmentFilter:
    min_cart_abandon_rate: Optional[float] = None
    max_cart_abandon_rate: Optional[float] = None
    min_spending_score: Optional[float] = None
    max_spending_score: Optional[float] = None
    country: Optional[str] = None


class MLService:
    def __init__(self):
        artifact = joblib.load(MODEL_PATH)
        self.pipeline = artifact["pipeline"]
        self.num_cols = artifact["num_cols"]
        self.cat_cols = artifact["cat_cols"]
        with open(METRICS_PATH) as f:
            self.metrics = json.load(f)
        self.df = pd.read_csv(DATA_PATH)

    def _filter(self, f: SegmentFilter) -> pd.DataFrame:
        d = self.df
        if f.min_cart_abandon_rate is not None:
            d = d[d["cart_abandon_rate"] >= f.min_cart_abandon_rate]
        if f.max_cart_abandon_rate is not None:
            d = d[d["cart_abandon_rate"] <= f.max_cart_abandon_rate]
        if f.min_spending_score is not None:
            d = d[d["spending_score"] >= f.min_spending_score]
        if f.max_spending_score is not None:
            d = d[d["spending_score"] <= f.max_spending_score]
        if f.country:
            d = d[d["country"].str.lower() == f.country.lower()]
        return d

    def score_segment(self, f: SegmentFilter) -> dict:
        segment = self._filter(f)
        if len(segment) == 0:
            return {
                "segment_size": 0,
                "mean_churn_probability": 0.0,
                "actual_churn_rate": None,
                **self._metric_payload(),
            }
        X = segment[self.num_cols + self.cat_cols]
        proba = self.pipeline.predict_proba(X)[:, 1]
        return {
            "segment_size": int(len(segment)),
            "mean_churn_probability": round(float(proba.mean()), 4),
            "actual_churn_rate": round(float(segment["churned"].mean()), 4),
            **self._metric_payload(),
        }

    def _metric_payload(self) -> dict:
        return {
            "model_precision": self.metrics["precision"],
            "model_recall": self.metrics["recall"],
            "model_f1": self.metrics["f1"],
            "model_roc_auc": self.metrics["roc_auc"],
            "model_name": self.metrics["model_name"],
            "disclaimer": DISCLAIMER,
        }

    def overall_churn_rate(self) -> float:
        return float(self.df["churned"].mean())

    def cohort_rate(self, f: SegmentFilter) -> Optional[float]:
        segment = self._filter(f)
        if len(segment) == 0:
            return None
        return float(segment["churned"].mean())

    def cohort_size(self, f: SegmentFilter) -> int:
        return int(len(self._filter(f)))


@lru_cache(maxsize=1)
def get_ml_service() -> "MLService":
    return MLService()
