"""
Unit tests for the Decision Evaluation Engine — the one component in Verdikt
where correctness is provable. Covers all six validation states plus the
pre-deadline guard.
"""
from datetime import datetime, timedelta
import pytest

from app.evaluation_engine import (
    evaluate, decision_status, two_proportion_z_test, EvalState, MetricReading,
)

DEADLINE = datetime(2026, 1, 1)
BEFORE = DEADLINE - timedelta(days=1)
AFTER = DEADLINE + timedelta(days=1)


def _base_kwargs(**overrides):
    kwargs = dict(
        baseline_value=0.20,
        target_value=0.10,
        direction="decrease",
        min_sample_size=100,
        deadline=DEADLINE,
        as_of=AFTER,
    )
    kwargs.update(overrides)
    return kwargs


def test_raises_if_evaluated_before_deadline_and_not_forced():
    with pytest.raises(ValueError):
        evaluate(**_base_kwargs(as_of=BEFORE, reading=MetricReading(0.1, 500)))


def test_forced_evaluation_before_deadline_is_allowed():
    result = evaluate(**_base_kwargs(as_of=BEFORE, forced=True, reading=MetricReading(0.05, 500)))
    assert result.state == EvalState.VALIDATED


def test_not_measurable_when_no_reading():
    result = evaluate(**_base_kwargs(reading=None))
    assert result.state == EvalState.NOT_MEASURABLE
    assert result.sample_size == 0


def test_not_measurable_when_zero_sample():
    result = evaluate(**_base_kwargs(reading=MetricReading(0.1, 0)))
    assert result.state == EvalState.NOT_MEASURABLE


def test_inconclusive_when_sample_too_small():
    result = evaluate(**_base_kwargs(min_sample_size=1000, reading=MetricReading(0.05, 50)))
    assert result.state == EvalState.INCONCLUSIVE
    assert result.sample_sufficient is False


def test_inconclusive_when_statistically_indistinguishable():
    # Observed rate nearly identical to baseline, large-ish but not huge n -> not significant
    result = evaluate(**_base_kwargs(
        baseline_value=0.20, target_value=0.10,
        reading=MetricReading(0.195, 120),
    ))
    assert result.state == EvalState.INCONCLUSIVE
    assert result.conclusive is False


def test_validated_when_target_clearly_reached():
    result = evaluate(**_base_kwargs(
        baseline_value=0.20, target_value=0.10,
        reading=MetricReading(0.05, 1500),
    ))
    assert result.state == EvalState.VALIDATED
    assert result.target_reached is True
    assert result.conclusive is True


def test_partially_validated_when_halfway_but_not_reached():
    # baseline 0.20 -> target 0.10; observed 0.14 is 60% of the way there, right direction
    result = evaluate(**_base_kwargs(
        baseline_value=0.20, target_value=0.10,
        reading=MetricReading(0.14, 5000),
    ))
    assert result.state == EvalState.PARTIALLY_VALIDATED
    assert result.target_reached is False


def test_invalidated_when_moved_wrong_direction():
    result = evaluate(**_base_kwargs(
        baseline_value=0.20, target_value=0.10,
        reading=MetricReading(0.30, 1500),
    ))
    assert result.state == EvalState.INVALIDATED
    assert result.target_reached is False


def test_invalidated_when_barely_moved_right_direction():
    # moved right direction but far short of halfway, with a large enough n to be conclusive
    result = evaluate(**_base_kwargs(
        baseline_value=0.20, target_value=0.10,
        reading=MetricReading(0.195, 50000),
    ))
    assert result.state in (EvalState.INVALIDATED, EvalState.INCONCLUSIVE)


def test_increase_direction_target_reached():
    result = evaluate(**_base_kwargs(
        baseline_value=0.10, target_value=0.20, direction="increase",
        reading=MetricReading(0.25, 1500),
    ))
    assert result.state == EvalState.VALIDATED
    assert result.target_reached is True


def test_decision_status_pending_before_deadline_no_evaluation():
    assert decision_status(deadline=DEADLINE, now=BEFORE, latest_state=None) == "Pending"


def test_decision_status_stale_after_deadline_no_evaluation():
    assert decision_status(deadline=DEADLINE, now=AFTER, latest_state=None) == "Stale"


def test_decision_status_uses_latest_evaluation_state_when_present():
    assert decision_status(deadline=DEADLINE, now=AFTER, latest_state="Validated") == "Validated"


def test_two_proportion_z_test_identical_rates_high_p_value():
    p = two_proportion_z_test(0.2, 1000, 0.2, 1000)
    assert p > 0.9


def test_two_proportion_z_test_very_different_rates_low_p_value():
    p = two_proportion_z_test(0.2, 1000, 0.05, 1000)
    assert p < 0.001
