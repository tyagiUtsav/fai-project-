# Verdikt

**Decision Debt OS, implemented.** Capture a business decision as an explicit,
falsifiable assumption, score its churn risk with a real trained model, and
let a rule-based engine check it against reality — assigning one of six
honest validation states: Validated, Partially Validated, Invalidated,
Inconclusive, Stale, or Not Measurable.

This repository is the working prototype that follows the Verdikt / Decision
Debt OS research phase (presentation deck, literature review, and the
original real-data churn analysis). It is not a mockup — every screen here
is backed by a running API, a real trained ML model, and a real SQL schema.

## Quickstart

**Backend**
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
python train_model.py        # trains + saves models/model.joblib (reproducible)
python -m app.seed           # loads the dataset, creates 7 demo decisions
uvicorn app.main:app --reload --port 8000
```

**Frontend** (separate terminal)
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**. The dashboard loads with 7 seeded decisions
spanning every validation state. Click into any of them, or go to "Capture a
Decision" to create a new one — the risk preview on that screen is scoring a
real customer segment with the real trained model as you type.

Run the test suite:
```bash
cd backend
pytest -q   # 24 tests: evaluation-engine logic (all 6 states) + API smoke tests
```

## Architecture

```
React + TypeScript (Vite)          FastAPI (Python)
┌─────────────────────┐            ┌──────────────────────────┐
│ Dashboard            │  REST/JSON │ /decisions   (CRUD)       │
│ Capture              │ ─────────▶ │ /decisions/{id}/evaluate  │
│ Decision Detail       │           │ /risk/score               │
└─────────────────────┘            └──────────┬────────────────┘
                                               │
                        ┌──────────────────────┼─────────────────────┐
                        ▼                      ▼                     ▼
                 evaluation_engine.py   ml_service.py          SQLAlchemy models
                 (pure, unit-tested     (loads trained RF      (Decision, Evaluation)
                  decision-table logic)  model + scores          — SQLite locally,
                                         any segment on demand)   Postgres-ready
```

This mirrors the 7-layer architecture from the research deck: the React app
is the User Interface + Decision Capture layer; `evaluation_engine.py` is
the Assumption & Metric layer + Outcome Evaluation Engine; `ml_service.py`
is the ML Risk-Prediction layer; the seed/CSV pipeline stands in for the
Data Integration layer (a real deployment would pull live product/billing
data instead); and the Dashboard screen is the Decision Debt Dashboard.

## What's real vs. simulated

**Real:**
- The churn-risk model is a genuinely trained `RandomForestClassifier`
  (300 trees, `class_weight="balanced"`, 80/20 stratified split,
  `random_state=42`) on the supplied `Customer_Transactions.csv`
  (10,000 synthetic-but-structured rows). Retrain it yourself with
  `python train_model.py` — it's fully reproducible.
- Every risk score and cohort rate shown in the UI is computed live against
  that real dataset and that real model — nothing is hardcoded.
- The Decision Evaluation Engine's statistical test (a two-proportion
  z-test, implemented from scratch with no external stats dependency) is a
  genuine significance test, not a placeholder.

**Simulated, and labeled as such in the UI:**
- There's no real pre/post-intervention split in the dataset (it's a single
  snapshot), so seeded decisions compare a *stated* baseline/forecast
  against the *real* cohort's actual churn rate as a stand-in for "the
  outcome." The Decision Detail screen marks every such evaluation
  `simulated: true` and shows a visible callout explaining this.
  The "Fast-forward & evaluate" button exists specifically because real
  deadlines can't be waited out in a demo — using it is an explicit,
  visible action, never silent.
- The seed decisions' narratives (owners, kill conditions) are illustrative
  demo content, not real company decisions.

**A note on metric consistency:** the model metrics shown live in this
prototype (Precision 0.28 / Recall 0.67 / F1 0.40 / ROC-AUC 0.84) differ
slightly from the figures in the original presentation deck (0.26 / 0.78 /
0.39 / 0.84). Both runs used identical code and hyperparameters; the drift
comes from a package-version difference between the environment the deck's
numbers were computed in and this one (RandomForest training is not
bit-for-bit reproducible across scikit-learn/BLAS versions even with a
fixed `random_state`). F1 and ROC-AUC barely moved; precision/recall traded
off along the same curve. Treat this prototype's live, reproducible numbers
as the current source of truth going forward.

## API reference (short form)

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness check |
| `GET` | `/decisions` | List decisions, optional `?state=` `&owner=` filters |
| `POST` | `/decisions` | Create a decision record |
| `GET` | `/decisions/{id}` | Fetch one decision + its latest evaluation |
| `POST` | `/decisions/{id}/evaluate` | Run the evaluation engine (`{"forced": true}` to fast-forward past the deadline for a demo) |
| `GET` | `/risk/score` | Ad-hoc churn-risk scoring for a customer segment (`min_cart_abandon_rate`, `max_cart_abandon_rate`, `min_spending_score`, `max_spending_score`, `country`) |

Interactive API docs (Swagger UI) are available at `http://localhost:8000/docs`
once the backend is running.

## Known limitations / explicitly out of scope for this prototype

- **No authentication or multi-tenancy.** Single-workspace, local-only, by
  design — this is an MVP prototype, not the roadmap's enterprise version.
- **No live data integration.** PostHog/Slack/CRM integrations are roadmap
  items; this prototype reads from the static seed CSV only.
- **No real pre/post-intervention measurement.** As noted above, "observed
  outcome" for a decision is the real dataset's current cohort rate, not a
  true before/after comparison — a real deployment would need an actual
  held-out control group.
- **SQLite only, locally.** The schema (`app/models.py`) is written against
  plain SQLAlchemy so pointing it at Postgres is a connection-string change,
  not a rewrite, but that hasn't been tested here.
- **No calibration analytics, metric ontology, or governance features** —
  these are the next three items on the roadmap from the original deck, and
  intentionally not built here.

## Roadmap (unchanged from the research phase)

```
This prototype → PostHog/Slack integration → calibration analytics →
metric ontology → enterprise governance
```

## Project layout

```
verdikt/
├── backend/
│   ├── app/
│   │   ├── main.py              FastAPI app + lifespan startup
│   │   ├── database.py          SQLAlchemy engine/session
│   │   ├── models.py            Decision, Evaluation ORM models
│   │   ├── schemas.py           Pydantic request/response schemas
│   │   ├── evaluation_engine.py Pure, unit-tested decision-table logic
│   │   ├── ml_service.py        Loads trained model, scores segments
│   │   ├── seed.py              Demo data loader (7 decisions, all 6 states)
│   │   └── routers/
│   │       ├── decisions.py
│   │       └── risk.py
│   ├── train_model.py           Reproducible model training script
│   ├── tests/                   24 tests: evaluation engine + API smoke
│   ├── data/Customer_Transactions.csv
│   └── models/                  model.joblib + metrics.json (generated)
└── frontend/
    └── src/
        ├── api.ts               Typed API client
        ├── App.tsx              Routing + sidebar nav
        └── pages/
            ├── Dashboard.tsx
            ├── Capture.tsx
            └── DecisionDetail.tsx
```
