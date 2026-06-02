# Analysis Patterns Reference — Live Developer Stack

## Exploratory Data Analysis (EDA) Workflow

Every analysis starts here. Don't skip steps.

```
1. Load data → 2. Shape & types → 3. Missing values → 4. Distributions → 5. Correlations → 6. Outliers → 7. Hypotheses
```

### Step-by-Step Template (pandas)

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Load ---
df = pd.read_csv("data.csv", parse_dates=["created_at"])

# --- 2. Shape & Types ---
print(f"Shape: {df.shape}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")

# --- 3. Missing Values ---
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(1)
print(f"\nMissing values:\n{pd.DataFrame({'count': missing, 'pct': missing_pct}).query('count > 0')}")

# --- 4. Distributions ---
df.describe()  # Numeric summary
df.select_dtypes(include="object").describe()  # Categorical summary

# --- 5. Correlations ---
corr = df.select_dtypes(include="number").corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.savefig("correlation_matrix.png", dpi=150)

# --- 6. Outliers ---
for col in df.select_dtypes(include="number").columns:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    outliers = df[(df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)]
    if len(outliers) > 0:
        print(f"  {col}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.1f}%)")

# --- 7. Hypotheses ---
# Document observations and formulate questions for deeper analysis
```

---

## Common Analysis Patterns

### Time Series Aggregation

```python
# Daily/weekly/monthly aggregation
daily = df.set_index("created_at").resample("D").agg({
    "revenue": "sum",
    "orders": "count",
    "avg_order_value": "mean",
})

# Rolling average (smooth out noise)
daily["revenue_7d_avg"] = daily["revenue"].rolling(7).mean()

# Year-over-year comparison
df["year"] = df["created_at"].dt.year
df["month"] = df["created_at"].dt.month
yoy = df.groupby(["year", "month"])["revenue"].sum().unstack(0)
```

### Cohort Analysis

```python
# Monthly cohort by sign-up month
df["cohort_month"] = df["signup_date"].dt.to_period("M")
df["activity_month"] = df["last_active"].dt.to_period("M")
df["months_since_signup"] = (df["activity_month"] - df["cohort_month"]).apply(lambda x: x.n)

cohort = df.groupby(["cohort_month", "months_since_signup"])["user_id"].nunique()
cohort_table = cohort.unstack()
cohort_pct = cohort_table.div(cohort_table[0], axis=0) * 100
```

### Funnel Analysis

```python
funnel_steps = ["visited", "signed_up", "activated", "paid"]

funnel_data = pd.DataFrame({
    "step": funnel_steps,
    "users": [10000, 3200, 1800, 450],
})
funnel_data["conversion_rate"] = (funnel_data["users"] / funnel_data["users"].iloc[0] * 100).round(1)
funnel_data["step_conversion"] = (funnel_data["users"] / funnel_data["users"].shift(1) * 100).round(1)
```

### Segmentation (RFM)

```python
# Recency, Frequency, Monetary
now = pd.Timestamp.now()
rfm = df.groupby("customer_id").agg({
    "order_date": lambda x: (now - x.max()).days,  # Recency
    "order_id": "count",                            # Frequency
    "total_amount": "sum",                          # Monetary
}).rename(columns={
    "order_date": "recency",
    "order_id": "frequency",
    "total_amount": "monetary",
})

# Score each dimension 1-5
for col in ["recency", "frequency", "monetary"]:
    rfm[f"{col}_score"] = pd.qcut(
        rfm[col], q=5, labels=[5, 4, 3, 2, 1] if col == "recency" else [1, 2, 3, 4, 5]
    )
```

---

## Statistical Methods

### Descriptive Statistics

```python
# Central tendency and spread
stats = df["metric"].agg(["mean", "median", "std", "min", "max", "count"])

# Percentiles
percentiles = df["metric"].quantile([0.25, 0.5, 0.75, 0.90, 0.95, 0.99])
```

### A/B Test Analysis

```python
from scipy import stats

# Two-sample t-test
control = df[df["variant"] == "control"]["metric"]
treatment = df[df["variant"] == "treatment"]["metric"]

t_stat, p_value = stats.ttest_ind(control, treatment)
effect_size = (treatment.mean() - control.mean()) / control.std()

print(f"Control mean: {control.mean():.3f}")
print(f"Treatment mean: {treatment.mean():.3f}")
print(f"Lift: {(treatment.mean() / control.mean() - 1) * 100:.1f}%")
print(f"p-value: {p_value:.4f} ({'Significant' if p_value < 0.05 else 'Not significant'})")
print(f"Effect size (Cohen's d): {effect_size:.3f}")
```

### Chi-Square Test (Categorical)

```python
from scipy.stats import chi2_contingency

contingency = pd.crosstab(df["segment"], df["converted"])
chi2, p_value, dof, expected = chi2_contingency(contingency)
print(f"Chi-square: {chi2:.2f}, p-value: {p_value:.4f}")
```

---

## ETL Pipeline Pattern

```python
from dataclasses import dataclass
from typing import Any
import structlog

logger = structlog.get_logger()

@dataclass
class ETLResult:
    rows_extracted: int
    rows_transformed: int
    rows_loaded: int
    errors: list[str]

async def run_etl(source: str, destination: str) -> ETLResult:
    errors = []

    # Extract
    logger.info("Extracting", source=source)
    raw_data = await extract(source)

    # Transform
    logger.info("Transforming", rows=len(raw_data))
    clean_data = []
    for row in raw_data:
        try:
            clean_data.append(transform_row(row))
        except ValueError as e:
            errors.append(f"Row {row.get('id')}: {e}")

    # Load
    logger.info("Loading", rows=len(clean_data), destination=destination)
    await load(clean_data, destination)

    return ETLResult(
        rows_extracted=len(raw_data),
        rows_transformed=len(clean_data),
        rows_loaded=len(clean_data),
        errors=errors,
    )
```

---

## Common Pitfalls

- **Correlation ≠ causation** — Always state this explicitly in findings.
- **Survivorship bias** — Analyzing only successful cases ignores those who left/failed.
- **Simpson's paradox** — Aggregated trends can reverse when you segment. Always check.
- **Small sample sizes** — State confidence intervals. Don't over-interpret n < 30.
- **Cherry-picking** — Show ALL the data, not just the data that supports the narrative.
- **Ignoring missing data** — Document how much is missing and how you handled it.
