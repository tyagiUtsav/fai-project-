"""Smoke tests for the core API surface, against an isolated throwaway DB."""
from datetime import datetime, timedelta, timezone


def _future_deadline(days=1):
    return (datetime.now(timezone.utc) + timedelta(days=days)).replace(tzinfo=None).isoformat()


def _past_deadline(days=1):
    return (datetime.now(timezone.utc) - timedelta(days=days)).replace(tzinfo=None).isoformat()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_risk_score_real_model(client):
    r = client.get("/risk/score", params={"min_cart_abandon_rate": 0.7, "max_spending_score": 25})
    assert r.status_code == 200
    body = r.json()
    assert body["segment_size"] > 0
    assert 0 <= body["mean_churn_probability"] <= 1
    assert body["model_precision"] > 0
    assert "disclaimer" in body


def test_create_and_fetch_decision(client):
    payload = {
        "title": "Test decision",
        "raw_text": "We believe X will reduce churn from 20% to 10%.",
        "owner": "Test Owner",
        "intervention": "Test intervention",
        "target_metric": "30-day churn rate",
        "baseline_value": 0.20,
        "target_value": 0.10,
        "direction": "decrease",
        "confidence": 0.6,
        "deadline": _future_deadline(),
        "kill_condition": "If churn > 25%, stop",
        "min_sample_size": 30,
        "filter_min_cart_abandon_rate": 0.7,
        "filter_max_spending_score": 25,
    }
    r = client.post("/decisions", json=payload)
    assert r.status_code == 201
    created = r.json()
    assert created["status"] == "Pending"

    r2 = client.get(f"/decisions/{created['id']}")
    assert r2.status_code == 200
    assert r2.json()["title"] == "Test decision"


def test_decision_reads_as_stale_after_deadline_with_no_evaluation(client):
    payload = {
        "title": "Stale test decision",
        "raw_text": "We believe Y will reduce churn from 20% to 10%.",
        "owner": "Test Owner",
        "intervention": "Test intervention",
        "target_metric": "30-day churn rate",
        "baseline_value": 0.20,
        "target_value": 0.10,
        "direction": "decrease",
        "confidence": 0.6,
        "deadline": _past_deadline(),
        "min_sample_size": 30,
        "filter_min_cart_abandon_rate": 0.7,
        "filter_max_spending_score": 25,
    }
    r = client.post("/decisions", json=payload)
    assert r.json()["status"] == "Stale"


def test_evaluate_decision_produces_a_state(client):
    payload = {
        "title": "Evaluate-me decision",
        "raw_text": "We believe Z will reduce churn from 25% to 15%.",
        "owner": "Test Owner",
        "intervention": "Test intervention",
        "target_metric": "30-day churn rate",
        "baseline_value": 0.25,
        "target_value": 0.15,
        "direction": "decrease",
        "confidence": 0.5,
        "deadline": _past_deadline(),
        "min_sample_size": 30,
        "filter_min_cart_abandon_rate": 0.7,
        "filter_max_spending_score": 25,
    }
    created = client.post("/decisions", json=payload).json()
    r = client.post(f"/decisions/{created['id']}/evaluate", json={"forced": True})
    assert r.status_code == 200
    body = r.json()
    assert body["latest_evaluation"] is not None
    assert body["status"] == body["latest_evaluation"]["state"]


def test_evaluate_not_measurable_for_nonexistent_segment(client):
    payload = {
        "title": "Not measurable decision",
        "raw_text": "We believe W will reduce churn in an unlaunched market.",
        "owner": "Test Owner",
        "intervention": "Test intervention",
        "target_metric": "30-day churn rate",
        "baseline_value": 0.20,
        "target_value": 0.10,
        "direction": "decrease",
        "confidence": 0.3,
        "deadline": _past_deadline(),
        "min_sample_size": 30,
        "filter_country": "Nowhereland",
    }
    created = client.post("/decisions", json=payload).json()
    r = client.post(f"/decisions/{created['id']}/evaluate", json={"forced": True})
    assert r.json()["latest_evaluation"]["state"] == "Not Measurable"


def test_evaluate_before_deadline_without_force_fails(client):
    payload = {
        "title": "Too-early decision",
        "raw_text": "We believe V will reduce churn from 20% to 10%.",
        "owner": "Test Owner",
        "intervention": "Test intervention",
        "target_metric": "30-day churn rate",
        "baseline_value": 0.20,
        "target_value": 0.10,
        "direction": "decrease",
        "confidence": 0.5,
        "deadline": _future_deadline(10),
        "min_sample_size": 30,
        "filter_min_cart_abandon_rate": 0.7,
    }
    created = client.post("/decisions", json=payload).json()
    r = client.post(f"/decisions/{created['id']}/evaluate", json={"forced": False})
    assert r.status_code == 400


def test_list_decisions_filterable_by_owner(client):
    r = client.get("/decisions", params={"owner": "Test Owner"})
    assert r.status_code == 200
    assert all(d["owner"] == "Test Owner" for d in r.json())
