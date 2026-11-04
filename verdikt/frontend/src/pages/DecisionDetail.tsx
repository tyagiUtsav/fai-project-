import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api, Decision } from "../api";
import StatusBadge from "../components/StatusBadge";

function fmtPct(v: number): string {
  return `${(v * 100).toFixed(1)}%`;
}

export default function DecisionDetail() {
  const { id } = useParams();
  const [decision, setDecision] = useState<Decision | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [evaluating, setEvaluating] = useState(false);

  function load() {
    if (!id) return;
    api
      .getDecision(Number(id))
      .then(setDecision)
      .catch((e) => setError(e.message));
  }

  useEffect(load, [id]);

  async function handleEvaluate(forced: boolean) {
    if (!decision) return;
    setEvaluating(true);
    try {
      const updated = await api.evaluateDecision(decision.id, forced);
      setDecision(updated);
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setEvaluating(false);
    }
  }

  if (error) return <div className="error-banner">{error}</div>;
  if (!decision) return <div className="loading">Loading…</div>;

  const deadlinePassed = new Date(decision.deadline).getTime() < Date.now();
  const ev = decision.latest_evaluation;

  return (
    <div>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 4 }}>
        <h1 style={{ marginBottom: 0 }}>{decision.title}</h1>
        <StatusBadge status={decision.status} />
      </div>
      <p className="subtitle">Owner: {decision.owner} · Created {new Date(decision.created_at).toLocaleDateString()}</p>

      <div className="card" style={{ marginBottom: 20, fontStyle: "italic", borderColor: "var(--cyan)" }}>
        “{decision.raw_text}”
      </div>

      <div className="grid grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <h2>Decision Record</h2>
          <Field label="Intervention" value={decision.intervention} />
          <Field label="Target metric" value={decision.target_metric} />
          <Field label="Baseline → Target" value={`${fmtPct(decision.baseline_value)} → ${fmtPct(decision.target_value)} (${decision.direction})`} />
          <Field label="Confidence" value={fmtPct(decision.confidence)} />
          <Field label="Deadline" value={new Date(decision.deadline).toLocaleString()} />
          <Field label="Min. sample size" value={String(decision.min_sample_size)} />
          <Field label="Kill condition" value={decision.kill_condition || "—"} />
        </div>

        <div className="card">
          <h2>Evaluation</h2>
          {ev ? (
            <>
              <Field label="State" value={<StatusBadge status={ev.state} />} />
              <Field label="Observed value" value={`${fmtPct(ev.observed_value)} (n=${ev.sample_size})`} />
              <Field label="Target reached?" value={ev.target_reached ? "Yes" : "No"} />
              <Field label="Sample sufficient?" value={ev.sample_sufficient ? "Yes" : "No"} />
              <Field label="Statistically conclusive?" value={ev.conclusive ? "Yes" : "No"} />
              {ev.p_value !== null && <Field label="p-value" value={ev.p_value.toFixed(4)} />}
              <Field label="Notes" value={ev.notes || "—"} />
              {ev.simulated && (
                <div className="callout" style={{ marginTop: 10 }}>
                  This evaluation was fast-forwarded for demo purposes, not triggered by a real elapsed deadline.
                </div>
              )}
            </>
          ) : (
            <p style={{ color: "var(--gray)" }}>
              Not evaluated yet.{" "}
              {deadlinePassed
                ? "The deadline has passed — this decision reads as Stale until someone reviews it."
                : "The deadline hasn't passed yet."}
            </p>
          )}

          <div style={{ marginTop: 16, display: "flex", gap: 10 }}>
            {!deadlinePassed && (
              <button className="btn btn-amber" disabled={evaluating} onClick={() => handleEvaluate(true)}>
                {evaluating ? "Evaluating…" : "Fast-forward & evaluate (demo)"}
              </button>
            )}
            {deadlinePassed && (
              <button className="btn" disabled={evaluating} onClick={() => handleEvaluate(true)}>
                {evaluating ? "Evaluating…" : ev ? "Re-run evaluation" : "Evaluate now"}
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="callout">
        A risk score or evaluation here reflects real model output and real segment data from the seed
        dataset — but this is a prototype's synthetic data, not a live production integration. See the README
        for what's real vs. simulated.
      </div>
    </div>
  );
}

function Field({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="field" style={{ marginBottom: 10 }}>
      <label style={{ marginBottom: 2 }}>{label}</label>
      <div style={{ fontSize: 14 }}>{value}</div>
    </div>
  );
}
