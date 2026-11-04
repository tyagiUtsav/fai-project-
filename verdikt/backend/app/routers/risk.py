"""Ad-hoc churn-risk segment scoring, used by the Capture screen's live preview."""
from fastapi import APIRouter, Query
from typing import Optional

from app import schemas
from app.ml_service import get_ml_service, SegmentFilter

router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("/score", response_model=schemas.RiskScoreResponse)
def score(
    min_cart_abandon_rate: Optional[float] = Query(None, ge=0, le=1),
    max_cart_abandon_rate: Optional[float] = Query(None, ge=0, le=1),
    min_spending_score: Optional[float] = Query(None, ge=0, le=100),
    max_spending_score: Optional[float] = Query(None, ge=0, le=100),
    country: Optional[str] = None,
):
    ml = get_ml_service()
    seg = SegmentFilter(
        min_cart_abandon_rate=min_cart_abandon_rate,
        max_cart_abandon_rate=max_cart_abandon_rate,
        min_spending_score=min_spending_score,
        max_spending_score=max_spending_score,
        country=country,
    )
    return ml.score_segment(seg)
