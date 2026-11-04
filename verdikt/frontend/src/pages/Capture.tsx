import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, RiskScoreResponse } from "../api";

function toDatetimeLocalDefault(daysFromNow: number): string {
  const d = new Date(Date.now() + daysFromNow * 86400000);
  return d.toISOString().slice(0, 16);
}

export default function Capture() {
  const navigate = useNavigate();

  const [rawText, setRawText] = useState(
    "We believe a 10% retention discount will reduce 30-day churn among high-risk customers from 25% to 18%."
  );
  const [title, setTitle] = useState("Retention discount for high-risk customers");
  const [owner, setOwner] = useState("");
  const [intervention, setIntervention] = useState("10% retention discount, auto-applied at checkout");
  const [targetMetric, setTargetMetric] = useState("30-day churn rate, high-risk cohort");
  const [baseline, setBaseline] = useState(0.25);
  const [target, setTarget] = useState(0.15);
  const [direction, setDirection] = useState<"decrease" | "increase">("decrease");
  const [confidence, setConfidence] = useState(0.6);
  const [deadline, setDeadline] = useState(toDatetimeLocalDefault(30));
  const [killCondition, setKillCondition] = useState("If interim churn > 25% at day 15, stop offer");
  const [minSampleSize, setMinSampleSize] = useState(200);

  const [minCartAbandon, setMinCartAbandon] = useState<string>("0.7");
  const [maxCartAbandon, setMaxCartAbandon] = useState<string>("");
  const [minSpendingScore, setMinSpendingScore] = useState<string>("");
  const [maxSpendingScore, setMaxSpendingScore] = useState<string>("25");
  const [country, setCountry] = useState<string>("");

  const [preview, setPreview] = useState<RiskScoreResponse | null>(null);
  const [previewError, setPreviewError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    const handle = setTimeout(() => {
      api
        .scoreRisk({
          min_cart_abandon_rate: minCartAbandon ? Number(minCartAbandon) : undefined,
          max_cart_abandon_rate: maxCartAbandon ? Number(maxCartAbandon) : undefined,
          min_spending_score: minSpendingScore ? Number(minSpendingScore) : undefined,
          max_spending_score: maxSpendingScore ? Number(maxSpendingScore) : undefined,
          country: country || undefined,
        })
        .then((r) => {
          setPreview(r);
          setPreviewError(null);
        })
        .catch((e) => setPreviewError(e.message));
    }, 350);
    return () => clearTimeout(handle);
  }, [minCartAbandon, maxCartAbandon, minSpendingScore, maxSpendingScore, country]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setSubmitError(null);
    try {
      const created = await api.createDecision({
        title,
        raw_text: rawText,
        owner,
        intervention,
        target_metric: targetMetric,
        baseline_value: baseline,
        target_value: target,
        direction,
        confidence,
        deadline: new Date(deadline).toISOString(),
        kill_condition: killCondition || undefined,
        min_sample_size: minSampleSize,
        filter_min_cart_abandon_rate: minCartAbandon ? Number(minCartAbandon) : undefined,
        filter_max_cart_abandon_rate: maxCartAbandon ? Number(maxCartAbandon) : undefined,
        filter_min_spending_score: minSpendingScore ? Number(minSpendingScore) : undefined,
        filter_max_spending_score: maxSpendingScore ? Number(maxSpendingScore) : undefined,
        filter_country: country || undefined,
      });
      navigate(`/decisions/${created.id}`);
    } catch (e) {
      setSubmitError((e as Error).message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <h1>Capture a Decision</h1>
      <p className="subtitle">
        Describe the decision in plain language, then confirm the structured fields it extracts into.
      </p>

      <div className="grid grid-2" style={{ alignItems: "start" }}>
        <form className="card" onSubmit={handleSubmit}>
          <div className="field">
            <label>Decision note (free text)</label>
            <textarea value={rawText} onChange={(e) => setRawText(e.target.value)} />
          </div>
          <div className="grid grid-2">
            <div className="field">
              <label>Title</label>
              <input value={title} onChange={(e) => setTitle(e.target.value)} required />
            </div>
            <div className="field">
              <label>Owner</label>
              <input
                value={owner}
                onChange={(e) => setOwner(e.target.value)}
                placeholder="Your name, team"
                required
              />
            </div>
          </div>
          <div className="field">
            <label>Intervention</label>
            <input value={intervention} onChange={(e) => setIntervention(e.target.value)} required />
          </div>
          <div className="field">
            <label>Target metric</label>
            <input value={targetMetric} onChange={(e) => setTargetMetric(e.target.value)} required />
          </div>
          <div className="grid grid-2">
            <div className="field">
              <label>Baseline value (0–1)</label>
              <input
                type="number" step="0.01" min={0} max={1}
                value={baseline} onChange={(e) => setBaseline(Number(e.target.value))}
              />
            </div>
            <div className="field">
              <label>Target value (0–1)</label>
              <input
                type="number" step="0.01" min={0} max={1}
                value={target} onChange={(e) => setTarget(Number(e.target.value))}
              />
            </div>
          </div>
          <div className="grid grid-2">
            <div className="field">
              <label>Direction</label>
              <select value={direction} onChange={(e) => setDirection(e.target.value as "decrease" | "increase")}>
                <option value="decrease">Metric should decrease</option>
                <option value="increase">Metric should increase</option>
              </select>
            </div>
            <div className="field">
              <label>Confidence (0–1)</label>
              <input
                type="number" step="0.05" min={0} max={1}
                value={confidence} onChange={(e) => setConfidence(Number(e.target.value))}
              />
              <div className="field-hint">Self-reported forecast probability — logged for calibration tracking.</div>
            </div>
          </div>
          <div className="grid grid-2">
            <div className="field">
              <label>Deadline</label>
              <input type="datetime-local" value={deadline} onChange={(e) => setDeadline(e.target.value)} />
            </div>
            <div className="field">
              <label>Minimum sample size</label>
              <input
                type="number" min={1}
                value={minSampleSize} onChange={(e) => setMinSampleSize(Number(e.target.value))}
              />
            </div>
          </div>
          <div className="field">
            <label>Kill condition</label>
            <input value={killCondition} onChange={(e) => setKillCondition(e.target.value)} />
          </div>

          <h2 style={{ marginTop: 24 }}>Target Segment</h2>
          <div className="grid grid-2">
            <div className="field">
              <label>Min cart-abandon rate</label>
              <input value={minCartAbandon} onChange={(e) => setMinCartAbandon(e.target.value)} placeholder="e.g. 0.7" />
            </div>
            <div className="field">
              <label>Max cart-abandon rate</label>
              <input value={maxCartAbandon} onChange={(e) => setMaxCartAbandon(e.target.value)} placeholder="e.g. 0.3" />
            </div>
            <div className="field">
              <label>Min spending score</label>
              <input value={minSpendingScore} onChange={(e) => setMinSpendingScore(e.target.value)} placeholder="e.g. 50" />
            </div>
            <div className="field">
              <label>Max spending score</label>
              <input value={maxSpendingScore} onChange={(e) => setMaxSpendingScore(e.target.value)} placeholder="e.g. 25" />
            </div>
          </div>
          <div className="field">
            <label>Country (optional)</label>
            <input value={country} onChange={(e) => setCountry(e.target.value)} placeholder="e.g. UK" />
          </div>

          {submitError && <div className="error-banner">{submitError}</div>}
          <button className="btn" type="submit" disabled={submitting}>
            {submitting ? "Creating…" : "Create Decision Record"}
          </button>
        </form>

        <div className="card">
          <h2>Live Risk Preview</h2>
          {previewError && <div className="error-banner">{previewError}</div>}
          {!preview && !previewError && <div className="loading">Scoring segment…</div>}
          {preview && (
            <>
              <div className="grid grid-2" style={{ marginBottom: 16 }}>
                <div className="metric-tile">
                  <div className="value">{preview.segment_size.toLocaleString()}</div>
                  <div className="label">Customers in segment</div>
                </div>
                <div className="metric-tile">
                  <div className="value">{(preview.mean_churn_probability * 100).toFixed(1)}%</div>
                  <div className="label">Mean predicted churn risk</div>
                </div>
              </div>
              {preview.actual_churn_rate !== null && (
                <p style={{ fontSize: 13, color: "var(--gray)" }}>
                  Real, observed churn rate for this exact segment in the dataset:{" "}
                  <strong style={{ color: "var(--white)" }}>
                    {(preview.actual_churn_rate * 100).toFixed(1)}%
                  </strong>
                </p>
              )}
              <div className="grid grid-4" style={{ marginBottom: 12 }}>
                <div className="metric-tile">
                  <div className="value">{preview.model_precision.toFixed(2)}</div>
                  <div className="label">Precision</div>
                </div>
                <div className="metric-tile">
                  <div className="value">{preview.model_recall.toFixed(2)}</div>
                  <div className="label">Recall</div>
                </div>
                <div className="metric-tile">
                  <div className="value">{preview.model_f1.toFixed(2)}</div>
                  <div className="label">F1</div>
                </div>
                <div className="metric-tile">
                  <div className="value">{preview.model_roc_auc.toFixed(2)}</div>
                  <div className="label">ROC-AUC</div>
                </div>
              </div>
              <div className="callout">{preview.disclaimer}</div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
