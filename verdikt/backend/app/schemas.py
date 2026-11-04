"""Pydantic I/O schemas for the Verdikt API."""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Literal


class DecisionCreate(BaseModel):
    title: str = Field(..., max_length=200)
    raw_text: str = Field(..., description="The original free-text decision note")
    owner: str
    intervention: str
    target_metric: str
    baseline_value: float = Field(..., ge=0, le=1)
    target_value: float = Field(..., ge=0, le=1)
    direction: Literal["decrease", "increase"] = "decrease"
    confidence: float = Field(..., ge=0, le=1)
    deadline: datetime
    kill_condition: Optional[str] = None
    min_sample_size: int = 30
    segment_filter: Optional[str] = None
    filter_min_cart_abandon_rate: Optional[float] = None
    filter_max_cart_abandon_rate: Optional[float] = None
    filter_min_spending_score: Optional[float] = None
    filter_max_spending_score: Optional[float] = None
    filter_country: Optional[str] = None


class EvaluationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    evaluated_at: datetime
    observed_value: float
    sample_size: int
    target_reached: bool
    sample_sufficient: bool
    conclusive: bool
    p_value: Optional[float]
    state: str
    notes: Optional[str]
    simulated: bool


class DecisionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    raw_text: str
    owner: str
    intervention: str
    target_metric: str
    baseline_value: float
    target_value: float
    direction: str
    confidence: float
    deadline: datetime
    kill_condition: Optional[str]
    min_sample_size: int
    segment_filter: Optional[str]
    filter_min_cart_abandon_rate: Optional[float] = None
    filter_max_cart_abandon_rate: Optional[float] = None
    filter_min_spending_score: Optional[float] = None
    filter_max_spending_score: Optional[float] = None
    filter_country: Optional[str] = None
    created_at: datetime
    status: str = "Pending"  # derived post-validation: latest evaluation state, or Pending / Stale
    latest_evaluation: Optional[EvaluationOut] = None


class EvaluateRequest(BaseModel):
    forced: bool = Field(False, description="Fast-forward past the deadline for demo purposes")
    as_of: Optional[datetime] = None


class RiskScoreRequest(BaseModel):
    min_cart_abandon_rate: Optional[float] = None
    max_cart_abandon_rate: Optional[float] = None
    min_spending_score: Optional[float] = None
    max_spending_score: Optional[float] = None
    country: Optional[str] = None


class RiskScoreResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    segment_size: int
    mean_churn_probability: float
    actual_churn_rate: Optional[float] = None
    model_precision: float
    model_recall: float
    model_f1: float
    model_roc_auc: float
    model_name: str
    disclaimer: str
