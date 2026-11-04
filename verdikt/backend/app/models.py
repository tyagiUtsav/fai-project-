"""SQLAlchemy ORM models for Verdikt's decision-to-outcome data store."""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


def utcnow():
    """Naive UTC datetime — SQLite has no native tz support, so the whole
    app stores and compares naive UTC timestamps consistently."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    raw_text = Column(Text, nullable=False)
    owner = Column(String(120), nullable=False)
    intervention = Column(String(300), nullable=False)
    target_metric = Column(String(200), nullable=False)
    baseline_value = Column(Float, nullable=False)
    target_value = Column(Float, nullable=False)
    direction = Column(String(10), nullable=False, default="decrease")  # "decrease" | "increase"
    confidence = Column(Float, nullable=False)  # 0.0 - 1.0 self-reported forecast probability
    deadline = Column(DateTime, nullable=False)
    kill_condition = Column(String(300), nullable=True)
    min_sample_size = Column(Integer, nullable=False, default=30)
    segment_filter = Column(String(300), nullable=True)  # human-readable cohort description
    filter_min_cart_abandon_rate = Column(Float, nullable=True)
    filter_max_cart_abandon_rate = Column(Float, nullable=True)
    filter_min_spending_score = Column(Float, nullable=True)
    filter_max_spending_score = Column(Float, nullable=True)
    filter_country = Column(String(60), nullable=True)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    evaluations = relationship("Evaluation", back_populates="decision", order_by="Evaluation.evaluated_at.desc()")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(Integer, ForeignKey("decisions.id"), nullable=False)
    evaluated_at = Column(DateTime, default=utcnow, nullable=False)
    observed_value = Column(Float, nullable=False)
    sample_size = Column(Integer, nullable=False)
    target_reached = Column(Boolean, nullable=False)
    sample_sufficient = Column(Boolean, nullable=False)
    conclusive = Column(Boolean, nullable=False)
    p_value = Column(Float, nullable=True)
    state = Column(String(30), nullable=False)
    notes = Column(Text, nullable=True)
    simulated = Column(Boolean, nullable=False, default=False)

    decision = relationship("Decision", back_populates="evaluations")
