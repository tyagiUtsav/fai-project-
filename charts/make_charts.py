import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import json, os

OUT = "/tmp/claude-0/-home-user/e0edc0c6-eb30-56ed-ad48-c2d1ce79cd97/scratchpad/charts"
os.makedirs(OUT, exist_ok=True)

with open("/tmp/claude-0/-home-user/e0edc0c6-eb30-56ed-ad48-c2d1ce79cd97/scratchpad/analysis/results.json") as f:
    R = json.load(f)

NAVY = "#FAF7F2"   # page background — soft ivory
PANEL = "#FFFFFF"  # card fill — white
BLUE = "#6C8EBF"   # dusty pastel blue
CYAN = "#4FAE97"   # muted pastel teal/sage
AMBER = "#D9A54C"  # muted pastel gold
WHITE = "#3A3542"  # primary text — warm charcoal-plum
GRAY = "#786F85"   # secondary text — muted mauve-gray
GRID = "#E3DCEF"   # gridlines — soft lavender-gray
RED = "#D97878"    # muted pastel coral
GRAY_DK = "#C3BCD0" # faint muted lavender-gray (for a 6th, de-emphasized wedge)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": WHITE,
    "axes.edgecolor": GRID,
    "axes.labelcolor": WHITE,
    "xtick.color": GRAY,
    "ytick.color": GRAY,
    "figure.facecolor": NAVY,
    "axes.facecolor": NAVY,
    "savefig.facecolor": NAVY,
})

def save(fig, name, w=8, h=4.5, dpi=220):
    fig.set_size_inches(w, h)
    fig.savefig(os.path.join(OUT, name), dpi=dpi, bbox_inches="tight", pad_inches=0.25, facecolor=NAVY)
    plt.close(fig)

# ---------- 1. Feature importance (RF) ----------
feats = R["feature_importance_top10"][:6]
labels_map = {
    "spending_score": "Spending score",
    "cart_abandon_rate": "Cart abandon rate",
    "website_visits_per_month": "Website visits / mo",
    "num_purchases": "Number of purchases",
    "avg_purchase_value": "Avg purchase value",
    "membership_years": "Membership years",
}
names = [labels_map.get(f[0], f[0]) for f in feats][::-1]
vals = [f[1] for f in feats][::-1]

fig, ax = plt.subplots()
colors = [CYAN if i == len(vals)-1 else BLUE for i in range(len(vals))]
bars = ax.barh(names, vals, color=colors, height=0.55, zorder=3)
for b, v in zip(bars, vals):
    ax.text(v + 0.006, b.get_y() + b.get_height()/2, f"{v*100:.1f}%", va="center",
            color=WHITE, fontsize=11, fontweight="bold")
ax.set_xlim(0, max(vals) * 1.28)
ax.set_xlabel("Relative importance (Random Forest)", fontsize=10, color=GRAY)
ax.grid(axis="x", color=GRID, linewidth=0.6, zorder=0)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(axis="y", length=0, labelsize=11)
ax.tick_params(axis="x", length=0, labelsize=9)
save(fig, "feature_importance.png", w=7.6, h=4.0)

# ---------- 2. Churn rate by risk segment (real data) ----------
d = R["dataset_description"]
segs = ["Low-risk\ncohort\n(n=1,494)", "Overall\npopulation\n(n=10,000)", "High-risk\ncohort\n(n=724)"]
rates = [1.5, 10.9, 37.2]  # low-risk, overall, high-risk (from real analysis)
colors = [CYAN, GRAY, AMBER]
fig, ax = plt.subplots()
bars = ax.bar(segs, rates, color=colors, width=0.5, zorder=3)
for b, v in zip(bars, rates):
    ax.text(b.get_x() + b.get_width()/2, v + 1.2, f"{v:.1f}%", ha="center",
            color=WHITE, fontsize=13, fontweight="bold")
ax.set_ylim(0, 45)
ax.set_ylabel("Actual 30-day churn rate", fontsize=10, color=GRAY)
ax.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
ax.spines[["top", "right"]].set_visible(False)
ax.spines[["left", "bottom"]].set_color(GRID)
ax.tick_params(axis="x", labelsize=10, length=0)
ax.tick_params(axis="y", length=0, labelsize=9)
save(fig, "churn_by_segment.png", w=7.0, h=4.2)

# ---------- 3. Confusion matrix (Random Forest, real) ----------
cm = np.array(R["random_forest"]["confusion_matrix"])  # [[TN,FP],[FN,TP]]
fig, ax = plt.subplots()
im = ax.imshow(cm, cmap="Blues", vmin=0, vmax=cm.max()*1.15)
labels = [["TN", "FP"], ["FN", "TP"]]
for i in range(2):
    for j in range(2):
        ax.text(j, i, f"{labels[i][j]}\n{cm[i,j]:,}", ha="center", va="center",
                 color=WHITE if cm[i,j] < cm.max()*0.6 else NAVY, fontsize=13, fontweight="bold")
ax.set_xticks([0,1]); ax.set_xticklabels(["Predicted: stays", "Predicted: churns"], fontsize=9, color=GRAY)
ax.set_yticks([0,1]); ax.set_yticklabels(["Actual: stays", "Actual: churns"], fontsize=9, color=GRAY)
ax.spines[:].set_visible(False)
ax.tick_params(length=0)
save(fig, "confusion_matrix.png", w=5.2, h=4.2)

# ---------- 4. Decision evaluation states (ILLUSTRATIVE / SIMULATED) ----------
states = ["Validated", "Invalidated", "Partially\nValidated", "Inconclusive", "Stale", "Not\nMeasurable"]
vals2 = [34, 21, 18, 14, 8, 5]  # illustrative simulated mix, sums to 100
colors2 = [CYAN, RED, BLUE, AMBER, GRAY, GRAY_DK]
fig, ax = plt.subplots()
wedges, _ = ax.pie(vals2, colors=colors2, startangle=90, counterclock=False,
                    wedgeprops=dict(width=0.42, edgecolor=NAVY, linewidth=3))
ax.text(0, 0, "Illustrative\nmix", ha="center", va="center", color=GRAY, fontsize=11)
legend_labels = [f"{s.replace(chr(10),' ')} — {v}%" for s, v in zip(states, vals2)]
ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1.02, 0.5),
          frameon=False, labelcolor=WHITE, fontsize=10)
ax.set_aspect("equal")
save(fig, "decision_states_donut.png", w=7.2, h=4.0)

# ---------- 5. Dataset preview ("screenshot" of real rows) ----------
import pandas as pd
df_raw = pd.read_csv("/root/.claude/uploads/e0edc0c6-eb30-56ed-ad48-c2d1ce79cd97/fe887add-Customer_Transactions.csv")
cols = ["customer_id", "age", "gender", "country", "annual_income", "spending_score", "cart_abandon_rate", "churned"]
preview_df = df_raw[cols].head(8).copy()
preview_df["annual_income"] = preview_df["annual_income"].apply(lambda v: f"{v:,}")
preview_df["cart_abandon_rate"] = preview_df["cart_abandon_rate"].round(2)
header_disp = ["ID", "Age", "Gender", "Country", "Income", "Spend\nScore", "Cart\nAbandon", "Churned"]

fig, ax = plt.subplots(figsize=(11.5, 3.3))
ax.axis("off")
tbl = ax.table(
    cellText=preview_df.values.tolist(),
    colLabels=header_disp,
    cellLoc="center",
    loc="center",
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
tbl.scale(1, 2.0)
n_rows = len(preview_df) + 1
for (r, c), cell in tbl.get_celld().items():
    cell.set_edgecolor(GRID)
    cell.set_linewidth(0.8)
    if r == 0:
        cell.set_facecolor(BLUE_DK if False else "#4A6C94")
        cell.set_text_props(color="#FFFFFF", fontweight="bold", fontsize=10)
    else:
        cell.set_facecolor(PANEL if r % 2 == 1 else "#F2EDFA")
        cell.set_text_props(color=WHITE)
        if c == 7:  # churned column
            val = preview_df.iloc[r-1]["churned"]
            cell.set_text_props(color=(RED if val == 1 else CYAN), fontweight="bold")
fig.savefig(os.path.join(OUT, "dataset_preview.png"), dpi=220, bbox_inches="tight", pad_inches=0.15, facecolor=NAVY)
plt.close(fig)

# ---------- 6. Signed correlation with churn (real data) ----------
corr = R["correlations"]
corr_labels_map = {
    "spending_score": "Spending score",
    "num_purchases": "Number of purchases",
    "avg_purchase_value": "Avg purchase value",
    "website_visits_per_month": "Website visits / mo",
    "membership_years": "Membership years",
    "age": "Age",
    "annual_income": "Annual income",
    "cart_abandon_rate": "Cart abandon rate",
}
items = sorted(corr.items(), key=lambda kv: abs(kv[1]))
names_c = [corr_labels_map.get(k, k) for k, _ in items]
vals_c = [v for _, v in items]
colors_c = [RED if v > 0 else CYAN for v in vals_c]

fig, ax = plt.subplots()
bars = ax.barh(names_c, vals_c, color=colors_c, height=0.55, zorder=3)
for b, v in zip(bars, vals_c):
    x = v + (0.008 if v >= 0 else -0.008)
    ax.text(x, b.get_y() + b.get_height()/2, f"{v:+.2f}", va="center",
            ha="left" if v >= 0 else "right", color=WHITE, fontsize=10, fontweight="bold")
ax.axvline(0, color=GRID, linewidth=1)
lo, hi = min(vals_c), max(vals_c)
ax.set_xlim(lo * 1.55, hi * 1.9 if hi > 0 else 0.05)
ax.set_xlabel("Correlation with churn  (coral = increases risk, teal = protective)", fontsize=9.5, color=GRAY)
ax.grid(axis="x", color=GRID, linewidth=0.6, zorder=0)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(axis="y", length=0, labelsize=10.5)
ax.tick_params(axis="x", length=0, labelsize=9)
save(fig, "correlation_chart.png", w=7.4, h=4.0)

print("Charts written to", OUT)
print(os.listdir(OUT))
