---
name: data-analysis-agent
description: >
  Data analysis, reporting, and visualization skill for extracting insights from structured
  and semi-structured data. Use this skill whenever the user asks to analyze data, create
  reports, build dashboards with real data, write complex queries, generate charts, perform
  statistical analysis, create ETL pipelines, or any task where the primary goal is
  understanding data and communicating findings. Trigger on: "analyze", "report", "chart",
  "graph", "metrics", "KPI", "data", "CSV", "Excel", "database query", "statistics",
  "trends", "forecast", "ETL", "pipeline", "visualization", "pandas", "SQL analysis",
  or any request about making sense of numbers.
version: 1.0.0
maintainer: Daniel Calisaya / Live Developer
---

# Data Analysis Agent Skill

This skill guides OPUS through data analysis workflows — from raw data exploration to
polished reports with actionable insights. Every output must be accurate, reproducible,
and communicate findings clearly to both technical and non-technical stakeholders.

---

## Agent Thinking Process

Before touching any data, execute this checklist:

1. **Classify the analysis** — Exploratory, diagnostic, predictive, or prescriptive?
2. **Understand the question** — What decision will this analysis inform?
3. **Identify the data sources** — Where is the data? Format? Quality? Volume?
4. **Define the output** — Report, chart, dashboard, dataset, or recommendation?
5. **Check for bias** — Is the sample representative? Are there confounding variables?
6. **Load the relevant reference** — Read the appropriate file in `references/`.

---

## Analysis Types

| Type | Goal | Reference |
|---|---|---|
| Exploratory (EDA) | Understand the data, find patterns | `references/analysis-patterns.md` |
| Diagnostic | Explain why something happened | `references/analysis-patterns.md` |
| Reporting | Summarize metrics for stakeholders | `references/reporting.md` |
| Visualization | Communicate findings visually | `references/reporting.md` |
| ETL / Data Pipeline | Transform and load data | `references/analysis-patterns.md` |
| Statistical Analysis | Hypothesis testing, correlations | `references/analysis-patterns.md` |

---

## Technology Matrix

| Context | Stack |
|---|---|
| Quick analysis / scripting | Python + pandas + matplotlib/plotly |
| Database queries | PostgreSQL (see `dev-code-agent/references/sql-postgresql.md`) |
| Interactive notebooks | Jupyter / Google Colab |
| Production dashboards | Chart.js (frontend) or Metabase |
| ETL pipelines | Python + SQLAlchemy + cron/Celery |
| Spreadsheet output | pandas → Excel (`openpyxl`) or CSV |

---

## Input Schema

| Field | Required | Type | Description |
|---|---|---|---|
| `task_description` | ✅ | string | What question are we answering? |
| `data_source` | ✅ | string | Where is the data? (DB table, CSV, API) |
| `output_format` | ❌ | string | Report, chart, CSV, dashboard, narrative |
| `audience` | ❌ | string | Technical team, executives, clients |
| `time_range` | ❌ | string | Date range for analysis |
| `comparison` | ❌ | string | Compare against what? (previous period, benchmark) |

---

## Structured Output Format

```
## Question
[Restate the analysis question in one sentence]

## Methodology
[Data sources, filters, transformations, and statistical methods used]

## Findings
[Key results — lead with the most important insight]

## Visualizations
[Charts, tables, or graphs that support the findings]

## Recommendations
[What should the stakeholder DO based on this data?]

## Data Quality Notes
[Any caveats: missing data, small sample, assumptions made]
```

---

## Quality Standards

- **Answer the question first** — Don't bury the insight. Lead with it.
- **Reproducible** — Every analysis must include the code or query that generated it.
- **Show your work** — Include methodology so others can validate.
- **Honest about limitations** — State sample sizes, missing data, and confidence levels.
- **Visual clarity** — Charts must have titles, axis labels, legends, and appropriate scales.
- **No misleading visuals** — Y-axis starts at zero (for bar charts). No truncated scales without disclosure.
- **Actionable** — End with a recommendation, not just a description.

---

## Chart Selection Guide

| Data Relationship | Chart Type | When to Use |
|---|---|---|
| Trend over time | Line chart | Continuous data, time series |
| Comparison | Bar chart (horizontal) | Comparing categories |
| Composition | Stacked bar / Pie | Parts of a whole (avoid pie for >5 segments) |
| Distribution | Histogram / Box plot | Understanding spread and outliers |
| Correlation | Scatter plot | Relationship between two variables |
| Ranking | Horizontal bar | Ordered comparison |
| KPI / Single metric | Big number card | Dashboard headline metrics |
| Geographic | Map / Choropleth | Location-based data |

---

## Reference Files

Load the relevant reference before acting:

- `references/analysis-patterns.md` — EDA workflow, pandas patterns, statistical methods, ETL
- `references/reporting.md` — Report templates, chart best practices, dashboard design, Excel output

---

# Changelog

## v1.0.0 — 2026-06
- Initial release. Foundation by Daniel Calisaya / Live Developer.
- Covers exploratory analysis, reporting, visualization, ETL.
- Chart selection guide and quality standards established.
