# Marketing A/B Testing & Conversion Analysis

Experimentation project using the public **Marketing A/B Testing** dataset. The data compares users shown advertising (`ad`) with a control group shown a public-service announcement (`psa`) and records whether they converted.

## Dataset

The uploaded dataset contains **588,101 users** with treatment/control assignment, conversion outcome, ad exposure count, and the day/hour of highest exposure.

## Business questions

- What are treatment and control conversion rates?
- What are the absolute and relative observed uplifts?
- Is the difference statistically significant?
- What is the 95% confidence interval for the conversion-rate difference?
- How does conversion vary by day and hour of highest exposure?

## Observed results

| Group | Users | Conversions | Conversion rate |
|---|---:|---:|---:|
| Ad | 564,577 | 14,423 | 2.55% |
| PSA | 23,524 | 420 | 1.79% |

The observed absolute conversion lift is **0.77 percentage points**, equivalent to a **43.1% relative uplift** versus the control rate.

A two-proportion z-test gives **z = 7.37** and **p ≈ 1.71 × 10⁻¹³**. The 95% confidence interval for the absolute lift is approximately **0.60 to 0.94 percentage points**. In this dataset, that provides strong evidence that conversion differs between the ad and PSA groups.

These results show association within this experiment; they do not include revenue, ad cost, or profitability because those fields are not present in the source data.

## Run locally

```bash
python -m venv .venv
pip install -r requirements.txt
python src/ab_test_analysis.py --input data/raw/marketing_AB.csv
```

The analysis generates group summaries, a two-proportion z-test, absolute and relative uplift, a 95% confidence interval, day/hour segment summaries, and a conversion chart.

## SQL

`sql/ab_test_analysis.sql` provides reusable group, day, and hour conversion queries.

## Repository results

- `results/group_summary.csv` contains treatment/control conversion results.
- `results/test_results.csv` contains the statistical test and confidence interval.
