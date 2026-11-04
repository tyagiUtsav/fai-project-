const CLASS_MAP: Record<string, string> = {
  Validated: "badge-validated",
  "Partially Validated": "badge-partially-validated",
  Invalidated: "badge-invalidated",
  Inconclusive: "badge-inconclusive",
  Stale: "badge-stale",
  "Not Measurable": "badge-not-measurable",
  Pending: "badge-pending",
};

export default function StatusBadge({ status }: { status: string }) {
  const cls = CLASS_MAP[status] ?? "badge-pending";
  return <span className={`badge ${cls}`}>{status}</span>;
}
