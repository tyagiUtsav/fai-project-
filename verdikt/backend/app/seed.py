"""
Seed script: loads the real dataset via the ML service and creates 7 demo
decisions spanning all six evaluation states plus a Pending example, so a
cold demo tells the whole product story without manual data entry.

Run:  python -m app.seed
"""
from datetime import datetime, timedelta, timezone

from app.database import SessionLocal, init_db
from app import models
from app.ml_service import get_ml_service, SegmentFilter
from app.evaluation_engine import evaluate, MetricReading

NOW = datetime.now(timezone.utc).replace(tzinfo=None)  # naive UTC, matching SQLite storage


def _create(db, **kwargs) -> models.Decision:
    d = models.Decision(**kwargs)
    db.add(d)
    db.commit()
    db.refresh(d)
    return d


def _force_evaluate(db, ml, d: models.Decision, as_of: datetime):
    seg = SegmentFilter(
        min_cart_abandon_rate=d.filter_min_cart_abandon_rate,
        max_cart_abandon_rate=d.filter_max_cart_abandon_rate,
        min_spending_score=d.filter_min_spending_score,
        max_spending_score=d.filter_max_spending_score,
        country=d.filter_country,
    )
    rate = ml.cohort_rate(seg)
    n = ml.cohort_size(seg)
    reading = MetricReading(observed_value=rate, sample_size=n) if rate is not None else None
    result = evaluate(
        baseline_value=d.baseline_value,
        target_value=d.target_value,
        direction=d.direction,
        min_sample_size=d.min_sample_size,
        reading=reading,
        deadline=d.deadline,
        as_of=as_of,
        forced=True,
    )
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
        simulated=True,
    )
    db.add(ev)
    db.commit()
    print(f"  -> {d.title!r}: {result.state.value}  (n={result.sample_size}, observed={result.observed_value:.3f})")


def run():
    init_db()
    ml = get_ml_service()
    db = SessionLocal()

    # Clear any prior seed data for idempotency
    db.query(models.Evaluation).delete()
    db.query(models.Decision).delete()
    db.commit()

    print("Seeding Verdikt demo decisions...")

    # 1. VALIDATED — genuinely low-risk cohort churns far below target
    d1 = _create(
        db,
        title="Loyalty perks for engaged, low-risk customers",
        raw_text="We believe offering loyalty perks to customers with low cart-abandon and "
                 "high spending score will keep their 30-day churn below 5%.",
        owner="Priya Nair, Retention Lead",
        intervention="Loyalty perks (early access + bonus points) for low-risk segment",
        target_metric="30-day churn rate, low-risk cohort",
        baseline_value=0.109, target_value=0.05, direction="decrease",
        confidence=0.7, deadline=NOW - timedelta(days=5),
        kill_condition="If churn > 10% at day 15, stop perks",
        min_sample_size=200, segment_filter="cart_abandon_rate < 0.3 and spending_score > 50",
        filter_max_cart_abandon_rate=0.3, filter_min_spending_score=50.0,
    )
    _force_evaluate(db, ml, d1, as_of=NOW)

    # 2. INVALIDATED — an overconfident forecast the real cohort disproves
    d2 = _create(
        db,
        title="Win-back email for high-cart-abandon customers",
        raw_text="We believe a win-back email campaign will reduce 30-day churn among "
                 "high-cart-abandon, low-spending customers from a 25% baseline to 15%.",
        owner="Marcus Chen, Growth",
        intervention="Automated win-back email sequence",
        target_metric="30-day churn rate, high-cart-abandon cohort",
        baseline_value=0.25, target_value=0.15, direction="decrease",
        confidence=0.55, deadline=NOW - timedelta(days=12),
        kill_condition="If churn > 30% at day 15, stop campaign",
        min_sample_size=200, segment_filter="cart_abandon_rate >= 0.7 and spending_score <= 25",
        filter_min_cart_abandon_rate=0.7, filter_max_spending_score=25.0,
    )
    _force_evaluate(db, ml, d2, as_of=NOW)

    # 3. PARTIALLY VALIDATED — moved meaningfully toward target, didn't cross it
    d3 = _create(
        db,
        title="Simplified checkout flow, company-wide",
        raw_text="We believe simplifying the checkout flow will reduce overall 30-day churn "
                 "from 15% to 8%.",
        owner="Ana Ferreira, Product",
        intervention="3-step checkout redesign",
        target_metric="30-day churn rate, all customers",
        baseline_value=0.15, target_value=0.08, direction="decrease",
        confidence=0.5, deadline=NOW - timedelta(days=8),
        kill_condition="If churn > 18% at day 15, roll back",
        min_sample_size=500, segment_filter="all customers",
    )
    _force_evaluate(db, ml, d3, as_of=NOW)

    # 4. INCONCLUSIVE — sample too small to trust, by design (min_sample_size set high)
    d4 = _create(
        db,
        title="Chatbot nudge for UK customers",
        raw_text="We believe a chatbot nudge will reduce 30-day churn among UK customers "
                  "from 12% to 8%.",
        owner="Tom Hughes, Growth",
        intervention="In-app chatbot nudge at day 20 of inactivity",
        target_metric="30-day churn rate, UK cohort",
        baseline_value=0.12, target_value=0.08, direction="decrease",
        confidence=0.4, deadline=NOW - timedelta(days=3),
        kill_condition="If churn > 15% at day 15, stop nudge",
        min_sample_size=5000,  # deliberately higher than the real UK cohort size
        segment_filter="country = UK",
        filter_country="UK",
    )
    _force_evaluate(db, ml, d4, as_of=NOW)

    # 5. NOT MEASURABLE — segment doesn't exist in the data yet
    d5 = _create(
        db,
        title="Localized app launch, new region",
        raw_text="We believe a localized app experience will reduce 30-day churn in our "
                  "not-yet-launched Brazil-North region from 20% to 10%.",
        owner="Lena Ortiz, International",
        intervention="Localized app (language + payment methods)",
        target_metric="30-day churn rate, Brazil-North region",
        baseline_value=0.20, target_value=0.10, direction="decrease",
        confidence=0.3, deadline=NOW - timedelta(days=1),
        kill_condition="If churn > 30% at day 15, pause rollout",
        min_sample_size=100, segment_filter="country = Brazil-North (not yet launched)",
        filter_country="Brazil-North",
    )
    _force_evaluate(db, ml, d5, as_of=NOW)

    # 6. STALE — deadline passed, nobody has reviewed it (no evaluation triggered)
    _create(
        db,
        title="Price-anchoring change on pricing page",
        raw_text="We believe a price-anchoring change on the pricing page will reduce "
                  "30-day churn from 20% to 12%.",
        owner="Sofia Petrov, Pricing",
        intervention="Add a higher-priced 'decoy' tier above the recommended plan",
        target_metric="30-day churn rate, all customers",
        baseline_value=0.20, target_value=0.12, direction="decrease",
        confidence=0.45, deadline=NOW - timedelta(days=20),
        kill_condition="If churn > 25% at day 15, remove decoy tier",
        min_sample_size=500, segment_filter="all customers",
    )
    print("  -> 'Price-anchoring change on pricing page': left un-evaluated -> reads as Stale")

    # 7. PENDING — deadline still in the future
    _create(
        db,
        title="Referral incentive for high-risk customers",
        raw_text="We believe a referral incentive will reduce 30-day churn among high-risk "
                  "customers from 30% to 20%.",
        owner="Priya Nair, Retention Lead",
        intervention="$10 credit for a successful referral, high-risk segment only",
        target_metric="30-day churn rate, high-risk cohort",
        baseline_value=0.30, target_value=0.20, direction="decrease",
        confidence=0.6, deadline=NOW + timedelta(days=20),
        kill_condition="If churn > 35% at day 15, stop incentive",
        min_sample_size=200, segment_filter="cart_abandon_rate >= 0.7 and spending_score <= 25",
        filter_min_cart_abandon_rate=0.7, filter_max_spending_score=25.0,
    )
    print("  -> 'Referral incentive for high-risk customers': deadline in the future -> reads as Pending")

    db.close()
    print("\nSeed complete: 7 decisions created, spanning Validated / Invalidated / "
          "Partially Validated / Inconclusive / Not Measurable / Stale / Pending.")


if __name__ == "__main__":
    run()
