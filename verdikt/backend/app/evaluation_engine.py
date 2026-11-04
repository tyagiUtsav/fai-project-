"""
Decision Evaluation Engine.

Pure, dependency-free logic that turns a Decision + an observed metric
reading into one of six honest validation states. No ML model lives here —
this module only compares a stated forecast against measured reality using
a real two-proportion statistical test, and is independently unit-testable.

Decision table (evaluated only once `as_of >= decision.deadline`, or when
explicitly forced for demo purposes):

    metric_data missing / n == 0        -> NOT_MEASURABLE
    sample_size < min_sample_size       -> INCONCLUSIVE
    sample_sufficient, not conclusive   -> INCONCLUSIVE   (could be chance)
    sample_sufficient, conclusive,
        target fully reached            -> VALIDATED
    sample_sufficient, conclusive,
        >= 50% of the way to target,
        in the right direction          -> PARTIALLY_VALIDATED
    sample_sufficient, conclusive,
        not reached / wrong direction   -> INVALIDATED

`STALE` is not produced here — it is a read-time status assigned to any
Decision whose deadline has passed with zero Evaluation rows (see
app/routers/decisions.py::decision_status). `PENDING` is the implicit
status of a Decision before its deadline and before any evaluation exists.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import math


class EvalState(str, Enum):
    VALIDATED = "Validated"
    PARTIALLY_VALIDATED = "Partially Validated"
    INVALIDATED = "Invalidated"
    INCONCLUSIVE = "Inconclusive"
    STALE = "Stale"
    NOT_MEASURABLE = "Not Measurable"
    PENDING = "Pending"


@dataclass
class MetricReading:
    """An aggregated, post-decision measurement of the target metric."""
    observed_value: float          # e.g. observed churn rate, 0.0-1.0
    sample_size: int                # number of customers/events the reading is based on


@dataclass
class EvaluationResult:
    state: EvalState
    target_reached: bool
    sample_sufficient: bool
    conclusive: bool
    p_value: float | None
    observed_value: float
    sample_size: int
    notes: str


def _normal_cdf(z: float) -> float:
    """Standard normal CDF via the error function (no scipy dependency)."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def two_proportion_z_test(p1: float, n1: int, p2: float, n2: int) -> float:
    """
    Two-proportion z-test, returns a two-tailed p-value.

    p1, n1: baseline (forecast-stated) rate and its assumed sample size.
    p2, n2: observed rate and its real sample size.

    A real, if simplified, significance test: used to decide whether an
    observed shift in the metric is distinguishable from chance noise, not
    whether the intervention caused it.
    """
    if n1 <= 0 or n2 <= 0:
        return 1.0
    p1 = min(max(p1, 1e-6), 1 - 1e-6)
    p2 = min(max(p2, 1e-6), 1 - 1e-6)
    p_pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    if se == 0:
        return 1.0
    z = (p2 - p1) / se
    p_value = 2 * (1 - _normal_cdf(abs(z)))
    return p_value


def evaluate(
    *,
    baseline_value: float,
    target_value: float,
    direction: str,
    min_sample_size: int,
    reading: MetricReading | None,
    deadline: datetime,
    as_of: datetime,
    forced: bool = False,
    baseline_sample_size: int = 500,
    alpha: float = 0.05,
) -> EvaluationResult:
    """
    Evaluate a single decision against a metric reading.

    Raises ValueError if `as_of` is before `deadline` and `forced` is False
    — a decision should not be marked Validated/Invalidated before its
    stated review window has actually elapsed, except when a demo
    explicitly fast-forwards time.
    """
    if as_of < deadline and not forced:
        raise ValueError(
            "Cannot evaluate before the decision's deadline unless forced=True "
            "(used only to fast-forward a demo)."
        )

    if reading is None or reading.sample_size == 0:
        return EvaluationResult(
            state=EvalState.NOT_MEASURABLE,
            target_reached=False,
            sample_sufficient=False,
            conclusive=False,
            p_value=None,
            observed_value=0.0,
            sample_size=0,
            notes="No metric data was available for this decision's segment at review time.",
        )

    sample_sufficient = reading.sample_size >= min_sample_size

    p_value = two_proportion_z_test(
        p1=baseline_value, n1=baseline_sample_size,
        p2=reading.observed_value, n2=reading.sample_size,
    )
    conclusive = sample_sufficient and p_value < alpha

    if direction == "decrease":
        moved_right_direction = reading.observed_value < baseline_value
        target_reached = reading.observed_value <= target_value
    else:
        moved_right_direction = reading.observed_value > baseline_value
        target_reached = reading.observed_value >= target_value

    span = abs(target_value - baseline_value)
    progress = abs(reading.observed_value - baseline_value) / span if span > 0 else 0.0
    halfway_or_more = moved_right_direction and progress >= 0.5

    if not sample_sufficient:
        state = EvalState.INCONCLUSIVE
        notes = (
            f"Sample size {reading.sample_size} is below the minimum "
            f"{min_sample_size} required to trust this result."
        )
    elif not conclusive:
        state = EvalState.INCONCLUSIVE
        notes = f"Observed shift is not statistically distinguishable from chance (p={p_value:.3f})."
    elif target_reached:
        state = EvalState.VALIDATED
        notes = f"Target metric reached (observed={reading.observed_value:.3f} vs target={target_value:.3f}, p={p_value:.3f})."
    elif halfway_or_more:
        state = EvalState.PARTIALLY_VALIDATED
        notes = (
            f"Moved {progress*100:.0f}% of the way toward the target in the right direction "
            f"but did not cross it (p={p_value:.3f})."
        )
    else:
        state = EvalState.INVALIDATED
        notes = f"No meaningful improvement toward the target was observed (p={p_value:.3f})."

    return EvaluationResult(
        state=state,
        target_reached=target_reached,
        sample_sufficient=sample_sufficient,
        conclusive=conclusive,
        p_value=p_value,
        observed_value=reading.observed_value,
        sample_size=reading.sample_size,
        notes=notes,
    )


def decision_status(
    *, deadline: datetime, now: datetime, latest_state: str | None
) -> str:
    """Read-time status for a decision with no fresh evaluation requested."""
    if latest_state:
        return latest_state
    if now > deadline:
        return EvalState.STALE.value
    return EvalState.PENDING.value
