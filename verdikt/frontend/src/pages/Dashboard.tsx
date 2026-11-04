import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { api, Decision } from "../api";
import StatusBadge from "../components/StatusBadge";

const ALL_STATES = [
  "Validated",
  "Partially Validated",
  "Invalidated",
  "Inconclusive",
  "Stale",
  "Not Measurable",
  "Pending",
];

export default function Dashboard() {
  const [decisions, setDecisions] = useState<Decision[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stateFilter, setStateFilter] = useState("");

  function load() {
    setLoading(true);
    api
      .listDecisions()
      .then(setDecisions)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }

  useEffect(load, []);

  const filtered = useMemo(
    () => (stateFilter ? decisions.filter((d) => d.status === stateFilter) : decisions),
    [decisions, stateFilter]
  );

  const counts = useMemo(() => {
    const c: Record<string, number> = {};
    for (const s of ALL_STATES) c[s] = 0;
    for (const d of decisions) c[d.status] = (c[d.status] ?? 0) + 1;
    return c;
  }, [decisions]);

  return (
    <div>
      <h1>Decision Dashboard</h1>
      <p className="subtitle">Every decision Verdikt is tracking, and what it's actually checking.</p>

      {error && <div className="error-banner">Couldn't load decisions: {error}</div>}

      <div className="grid grid-4" style={{ marginBottom: 24 }}>
        {ALL_STATES.slice(0, 4).map((s) => (
          <div className="metric-tile" key={s}>
            <div className="value">{counts[s] ?? 0}</div>
            <div className="label">{s}</div>
          </div>
        ))}
      </div>

      <div className="filters">
        <select value={stateFilter} onChange={(e) => setStateFilter(e.target.value)}>
          <option value="">All states</option>
          {ALL_STATES.map((s) => (
            <option key={s} value={s}>
              {s} ({counts[s] ?? 0})
            </option>
          ))}
        </select>
        <button className="btn btn-secondary" onClick={load}>
          Refresh
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading decisions…</div>
      ) : (
        <div className="card" style={{ padding: 0 }}>
          <table>
            <thead>
              <tr>
                <th>Decision</th>
                <th>Owner</th>
                <th>Target Metric</th>
                <th>Deadline</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((d) => (
                <tr key={d.id} className="row-link">
                  <td>
                    <Link to={`/decisions/${d.id}`}>{d.title}</Link>
                  </td>
                  <td>{d.owner}</td>
                  <td>{d.target_metric}</td>
                  <td>{new Date(d.deadline).toLocaleDateString()}</td>
                  <td>
                    <StatusBadge status={d.status} />
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={5} style={{ color: "var(--gray)", textAlign: "center", padding: 24 }}>
                    No decisions match this filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
