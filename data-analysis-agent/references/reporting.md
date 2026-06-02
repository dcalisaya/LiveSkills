# Reporting & Visualization Reference — Live Developer Stack

## Report Structure

Every report follows this skeleton:

```
## Executive Summary          ← 2-3 sentences for busy stakeholders
## Key Metrics                ← Big numbers with trend indicators
## Detailed Findings          ← Charts, tables, narrative
## Recommendations            ← What to DO based on the data
## Methodology & Data Notes   ← Reproducibility and caveats
```

---

## Report Templates

### Weekly Performance Report

```markdown
# Weekly Report — [Project/Product] — Week of [Date]

## Summary
[One paragraph: overall trend, biggest win, biggest concern]

## Key Metrics

| Metric | This Week | Last Week | Change | Target |
|---|---|---|---|---|
| Revenue | $12,400 | $11,200 | +10.7% ✅ | $12,000 |
| Active Users | 1,245 | 1,180 | +5.5% ✅ | 1,200 |
| Churn Rate | 3.2% | 2.8% | +0.4pp ⚠️ | < 3% |
| NPS Score | 42 | 45 | -3 ⚠️ | > 40 |

## Highlights
- [Key accomplishment 1]
- [Key accomplishment 2]

## Concerns
- [Issue 1 — what's being done about it]
- [Issue 2 — what's being done about it]

## Next Week Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```

### Monthly Business Review

```markdown
# Monthly Review — [Month Year]

## Executive Summary
[3 sentences: performance vs targets, key initiative progress, outlook]

## Financial Overview
[Revenue, costs, margin, runway — table format]

## Product Metrics
[Users, engagement, retention, feature adoption — charts]

## Marketing Performance
[Traffic, leads, conversion, CAC — charts]

## Operations
[Uptime, incidents, deploy frequency, team velocity]

## Strategic Initiatives
| Initiative | Status | Progress | Next Milestone |
|---|---|---|---|

## Risks & Mitigations
| Risk | Impact | Probability | Mitigation |
|---|---|---|---|

## Decisions Needed
[List any decisions that require stakeholder input]
```

---

## Chart Best Practices

### General Rules

- **Title every chart** — Descriptive, not generic. "Revenue by Region Q2 2026" not "Chart 1"
- **Label axes** — Include units ($ , %, count, hours)
- **Start Y-axis at zero** for bar charts (prevents visual distortion)
- **Use consistent colors** across related charts
- **Limit to 5-7 series** per chart — more becomes noise
- **Include the source** — "Source: LiveApp database, 2026-06-01"

### Chart.js Template (Web Dashboard)

```javascript
const ctx = document.getElementById('revenueChart')
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
      label: 'Revenue ($)',
      data: [8200, 9100, 8800, 11200, 12400, 13100],
      borderColor: '#e8ff00',
      backgroundColor: 'rgba(232, 255, 0, 0.1)',
      fill: true,
      tension: 0.3,
      pointRadius: 4,
      pointBackgroundColor: '#e8ff00',
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Monthly Revenue — H1 2026',
        color: '#f0f0f0',
        font: { size: 16, family: 'DM Sans', weight: '600' },
      },
      legend: { labels: { color: '#a0a0a0', font: { family: 'DM Sans' } } },
    },
    scales: {
      x: { ticks: { color: '#8a8a8a' }, grid: { color: '#1e1e1e' } },
      y: {
        ticks: {
          color: '#8a8a8a',
          callback: (v) => `$${(v / 1000).toFixed(0)}k`,
        },
        grid: { color: '#1e1e1e' },
        beginAtZero: true,
      },
    },
  },
})
```

### Matplotlib / Seaborn Template (Reports)

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Live Developer style
plt.style.use("dark_background")
COLORS = {
    "accent": "#e8ff00",
    "accent_muted": "#b8cc00",
    "text": "#f0f0f0",
    "muted": "#8a8a8a",
    "surface": "#161616",
    "bg": "#0d0d0d",
}

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor(COLORS["bg"])
ax.set_facecolor(COLORS["surface"])

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
revenue = [8200, 9100, 8800, 11200, 12400, 13100]

ax.plot(months, revenue, color=COLORS["accent"], linewidth=2, marker="o", markersize=6)
ax.fill_between(months, revenue, alpha=0.1, color=COLORS["accent"])

ax.set_title("Monthly Revenue — H1 2026", fontsize=14, color=COLORS["text"], pad=16)
ax.set_ylabel("Revenue ($)", color=COLORS["muted"])
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
ax.tick_params(colors=COLORS["muted"])
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.15)

plt.tight_layout()
plt.savefig("revenue_h1_2026.png", dpi=150, bbox_inches="tight")
```

---

## Data Tables (Markdown/HTML)

### Formatting Rules

- **Right-align numbers** — currencies, percentages, counts
- **Left-align text** — names, descriptions, categories
- **Bold totals and headers**
- **Use color indicators** — ✅ on target, ⚠️ warning, ❌ off track
- **Sort by most important column** — usually the primary metric, descending

### KPI Dashboard Cards

```
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│  ACTIVE PROJECTS    │  │  DELIVERABLES DONE   │  │  AVG CYCLE TIME     │
│        24           │  │       142            │  │      2.5 days       │
│   +3 this week ✅   │  │  +18 this month ✅   │  │  -1.2 days ✅       │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

---

## Excel / CSV Output

```python
import pandas as pd
from datetime import datetime

def export_report(df: pd.DataFrame, report_name: str) -> str:
    """Export DataFrame to formatted Excel with Live Developer styling."""
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"reports/{report_name}_{timestamp}.xlsx"

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        # Main data
        df.to_excel(writer, sheet_name="Data", index=False)

        # Summary stats
        summary = df.describe()
        summary.to_excel(writer, sheet_name="Summary")

        # Format
        workbook = writer.book
        for sheet in workbook.worksheets:
            for col in sheet.columns:
                max_length = max(len(str(cell.value or "")) for cell in col)
                sheet.column_dimensions[col[0].column_letter].width = min(max_length + 4, 40)

    return filename
```

---

## Dashboard Design Principles

When building a data dashboard (see also `frontend-ui-agent/references/dashboards.md`):

1. **Most important metric at the top left** — eye reads left-to-right, top-to-bottom.
2. **Max 6 KPI cards** above the fold — more is cognitive overload.
3. **One primary chart** per section — support with a data table below if needed.
4. **Time filters always visible** — date range selector at the top.
5. **Comparison context** — always show vs previous period, vs target, or vs benchmark.
6. **Drill-down capability** — click a card to see the detail, not everything at once.

---

## Common Pitfalls

- **Too much data, no insight** — A report is not a data dump. Lead with the conclusion.
- **Missing context** — "Revenue is $12k" means nothing. "$12k vs $10k target (+20%)" means everything.
- **Wrong chart type** — Pie charts for trends. Line charts for categories. Match data to visual.
- **No time context** — Always specify the period. "We have 1,200 users" → since when?
- **Vanity metrics** — Total page views without conversion context is misleading. Focus on actionable metrics.
