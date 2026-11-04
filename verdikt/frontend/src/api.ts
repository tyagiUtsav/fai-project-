// API client + types for the Verdikt backend. All business logic stays on
// the server — this file only shapes requests/responses.

const BASE = "/api";

export interface Evaluation {
  id: number;
  evaluated_at: string;
  observed_value: number;
  sample_size: number;
  target_reached: boolean;
  sample_sufficient: boolean;
  conclusive: boolean;
  p_value: number | null;
  state: string;
  notes: string | null;
  simulated: boolean;
}

export interface Decision {
  id: number;
  title: string;
  raw_text: string;
  owner: string;
  intervention: string;
  target_metric: string;
  baseline_value: number;
  target_value: number;
  direction: "decrease" | "increase";
  confidence: number;
  deadline: string;
  kill_condition: string | null;
  min_sample_size: number;
  segment_filter: string | null;
  filter_min_cart_abandon_rate: number | null;
  filter_max_cart_abandon_rate: number | null;
  filter_min_spending_score: number | null;
  filter_max_spending_score: number | null;
  filter_country: string | null;
  created_at: string;
  status: string;
  latest_evaluation: Evaluation | null;
}

export interface DecisionCreate {
  title: string;
  raw_text: string;
  owner: string;
  intervention: string;
  target_metric: string;
  baseline_value: number;
  target_value: number;
  direction: "decrease" | "increase";
  confidence: number;
  deadline: string;
  kill_condition?: string;
  min_sample_size: number;
  segment_filter?: string;
  filter_min_cart_abandon_rate?: number;
  filter_max_cart_abandon_rate?: number;
  filter_min_spending_score?: number;
  filter_max_spending_score?: number;
  filter_country?: string;
}

export interface RiskScoreResponse {
  segment_size: number;
  mean_churn_probability: number;
  actual_churn_rate: number | null;
  model_precision: number;
  model_recall: number;
  model_f1: number;
  model_roc_auc: number;
  model_name: string;
  disclaimer: string;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API error ${res.status}: ${body}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  listDecisions: (params?: { state?: string; owner?: string }) => {
    const qs = new URLSearchParams();
    if (params?.state) qs.set("state", params.state);
    if (params?.owner) qs.set("owner", params.owner);
    const suffix = qs.toString() ? `?${qs.toString()}` : "";
    return request<Decision[]>(`/decisions${suffix}`);
  },
  getDecision: (id: number) => request<Decision>(`/decisions/${id}`),
  createDecision: (payload: DecisionCreate) =>
    request<Decision>("/decisions", { method: "POST", body: JSON.stringify(payload) }),
  evaluateDecision: (id: number, forced: boolean) =>
    request<Decision>(`/decisions/${id}/evaluate`, {
      method: "POST",
      body: JSON.stringify({ forced }),
    }),
  scoreRisk: (params: {
    min_cart_abandon_rate?: number;
    max_cart_abandon_rate?: number;
    min_spending_score?: number;
    max_spending_score?: number;
    country?: string;
  }) => {
    const qs = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") qs.set(k, String(v));
    });
    return request<RiskScoreResponse>(`/risk/score?${qs.toString()}`);
  },
};
