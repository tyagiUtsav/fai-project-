"""Decision CRUD + evaluation-trigger endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone


def _naive_utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)
from typing import Optional, List

from app.database import get_db
from app import models, schemas
from app.evaluation_engine import evaluate, decision_status, MetricReading
from app.ml_service import get_ml_service, SegmentFilter

router = APIRouter(prefix="/decisions", tags=["decisions"])


def _to_out(d: models.Decision) -> schemas.DecisionOut:
    latest = d.evaluations[0] if d.evaluations else None
    now = _naive_utc_now()
    deadline = d.deadline.replace(tzinfo=None) if d.deadline.tzinfo else d.deadline
    status = decision_status(
        deadline=deadline, now=now, latest_state=latest.state if latest else None
    )
    out = schemas.DecisionOut.model_validate(d)
    out.status = status
    out.latest_evaluation = schemas.EvaluationOut.model_validate(latest) if latest else None
    return out


@router.post("", response_model=schemas.DecisionOut, status_code=201)
def create_decision(payload: schemas.DecisionCreate, db: Session = Depends(get_db)):
    d = models.Decision(**payload.model_dump())
    db.add(d)
    db.commit()
    db.refresh(d)
    return _to_out(d)


@router.get("", response_model=List[schemas.DecisionOut])
def list_decisions(
    state: Optional[str] = None,
    owner: Optional[str] = None,
    db: Session = Depends(get_db),
):
    decisions = db.query(models.Decision).order_by(models.Decision.created_at.desc()).all()
    out = [_to_out(d) for d in decisions]
    if state:
        out = [d for d in out if d.status.lower() == state.lower()]
    if owner:
        out = [d for d in out if d.owner.lower() == owner.lower()]
    return out


@router.get("/{decision_id}", response_model=schemas.DecisionOut)
def get_decision(decision_id: int, db: Session = Depends(get_db)):
    d = db.get(models.Decision, decision_id)
    if not d:
        raise HTTPException(404, "Decision not found")
    return _to_out(d)


@router.post("/{decision_id}/evaluate", response_model=schemas.DecisionOut)
def evaluate_decision(
    decision_id: int, payload: schemas.EvaluateRequest, db: Session = Depends(get_db)
):
    d = db.get(models.Decision, decision_id)
    if not d:
        raise HTTPException(404, "Decision not found")

    ml = get_ml_service()
    seg = SegmentFilter(
        min_cart_abandon_rate=d.filter_min_cart_abandon_rate,
        max_cart_abandon_rate=d.filter_max_cart_abandon_rate,
        min_spending_score=d.filter_min_spending_score,
        max_spending_score=d.filter_max_spending_score,
        country=d.filter_country,
    )
    observed_rate = ml.cohort_rate(seg)
    observed_n = ml.cohort_size(seg)
    reading = MetricReading(observed_value=observed_rate, sample_size=observed_n) if observed_rate is not None else None

    deadline = d.deadline.replace(tzinfo=None) if d.deadline.tzinfo else d.deadline
    as_of = payload.as_of or _naive_utc_now()
    if as_of.tzinfo is not None:
        as_of = as_of.replace(tzinfo=None)

    try:
        result = evaluate(
            baseline_value=d.baseline_value,
            target_value=d.target_value,
            direction=d.direction,
            min_sample_size=d.min_sample_size,
            reading=reading,
            deadline=deadline,
            as_of=as_of,
            forced=payload.forced,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

    ev = models.Evaluation(
        decision_id=d.id,
        observed_value=result.observed_value,
        sample_size=result.sample_size,
        target_reached=result.target_reached,
        sample_sufficient=result.sample_sufficient,
        conclusive=result.conclusive,
        p_value=result.p_value,
        state=result.state.value,
        notes=result.notes,
        simulated=payload.forced,
    )
    db.add(ev)
    db.commit()
    db.refresh(d)
    return _to_out(d)
